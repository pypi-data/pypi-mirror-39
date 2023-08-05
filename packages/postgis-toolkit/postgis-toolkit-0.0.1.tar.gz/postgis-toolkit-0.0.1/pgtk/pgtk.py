#!/usr/bin/env python3

import csv
import os
import subprocess

import click
import psycopg2
from tabulate import tabulate


class Connection(object):
    def __init__(self, host, port, dbname, user, schema, crs):
        try:
            self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, port=port)
        except psycopg2.OperationalError as e:
            print(e)
            exit()
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.schema = schema
        self.crs = crs


@click.group()
@click.option("--host", '-h', required=False, default='localhost',
              help="hostname")
@click.option("--port", '-p', required=False, default='5432',
              help="port number")
@click.option("--dbname", '-d', required=False, default='postgres',
              help="database")
@click.option("--user", '-u', required=False, default='postgres',
              help="user")
@click.option("--schema", '-s', required=False, default='public',
              help="database schema")
@click.option("--crs", '-c', required=False, default='4326',
              help="EPSG code")
@click.pass_context
def cli(ctx, host, port, dbname, user, schema, crs):
    """PostGIS Commands"""
    ctx.obj = Connection(host, port, dbname, user, schema, crs)


@cli.group('layers')
def layers():
    """Layer commands"""
    pass


@layers.command("list")
@click.pass_obj
def list_layers(ctx):
    """List data tables"""
    tables = get_data_tables()
    print(f'--- {ctx.schema}.{ctx.dbname} ---')
    for table in tables:
        print(f' * {table}')


@layers.command("preview")
@click.option("-n", required=False, default=1, help="count")
@click.argument("table", required=True)
@click.pass_obj
def preview_layers(ctx, table, n):
    """Preview data table"""
    print(f'--- preview {table} ---')
    cur = ctx.conn.cursor()
    sql = f"""SELECT * FROM {table} LIMIT {n}"""
    cur.execute(sql)
    cols = [desc[0] for desc in cur.description]
    result = cur.fetchmany(n)
    print(tabulate(result, cols, tablefmt="plain"))


@layers.command("delete")
@click.argument("table", nargs=-1, required=True)
@click.pass_obj
def delete_layer(ctx, table):
    """Delete table"""
    print(f'--- delete {table} ---')
    cur = ctx.conn.cursor()
    for t in table:
        if not table_exists(t):
            print(f'NOTICE:  table "{t}" does not exist, skipping')
            continue
        sql = f"""DROP TABLE IF EXISTS {t};"""
        cur.execute(sql)
    ctx.conn.commit()


@layers.command("copy")
@click.argument("table", required=True)
@click.argument("name", required=True)
@click.pass_obj
def copy_layer(ctx, table, name):
    """Copy table"""
    print(f'--- copy {table} >> {name} ---')
    if not table_exists(table):
        print(f'NOTICE:  table "{table}" does not exist')
        return None
    cur = ctx.conn.cursor()
    sql = f"""SELECT * INTO {name} FROM {table}"""
    cur.execute(sql)
    ctx.conn.commit()


@cli.command('import')
@click.option("--file", "-f",
              type=click.Path(file_okay=True, exists=True),
              required=False, default=os.getcwd(),
              help='target file or directory')
@click.option("--driver", type=click.Choice(["shapefile", "csv", "tsv"]),
              required=False, default='shapefile')
def import_command(file, driver):
    """Import data to PostgreSQL"""
    print(f'--- import {driver} ---')
    geo_files = get_geo_files(file, driver)
    if not geo_files:
        print('NOTICE: nothing to import')
        return
    for geo_file in geo_files:
        table = os.path.basename(geo_file)[:-4].lower()
        if table_exists(table):
            print(f"NOTICE: table '{table}' already exists, skipping")
            continue
        if driver == 'shapefile':
            import_shapefile(geo_file)
        elif driver == 'csv':
            import_csv_file(geo_file, delimiter=",")
        elif driver == 'tsv':
            import_csv_file(geo_file, delimiter="\t")


@click.pass_obj
def import_csv_file(ctx, csv_file, delimiter):
    print(f'>> {os.path.basename(csv_file)}')
    with open(csv_file) as fin:
        csv_reader = csv.reader(fin, delimiter=delimiter)
        csv_header = next(csv_reader)
    table = os.path.basename(csv_file)[:-4]
    cur = ctx.conn.cursor()
    sql = f"""CREATE TABLE {table} ({','.join([h + ' varchar' for h in csv_header])});"""
    try:
        cur.execute(sql)
    except psycopg2.ProgrammingError as e:
        print('NOTICE: Bad Header, skipping')
        print(e)
        return
    ctx.conn.commit()
    if delimiter == "\t":
        delimiter = "E'\t'"
    elif delimiter == ",":
        delimiter = "','"
    cmd = ['psql', '-h', ctx.host,
           '-d', ctx.dbname, '-U', ctx.user, '-p', ctx.port,
           '-c',  f"\\copy {table} FROM '{csv_file}' DELIMITER {delimiter} CSV HEADER"]
    subprocess.run(cmd)


@click.pass_obj
def import_shapefile(ctx, shapefile):
        print(f'>> {os.path.basename(shapefile)}')
        cmd1 = ['/usr/local/bin/shp2pgsql', '-I', '-s',
                ctx.crs, shapefile, f'{ctx.schema}.{os.path.basename(shapefile)[:-4]}']
        cmd2 = ['psql', '-U', ctx.user, '-p', ctx.port,
                '-h', ctx.host, '-d', ctx.dbname]
        shp2pgsql = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        psql = subprocess.Popen(cmd2, stdin=shp2pgsql.stdout, stdout=subprocess.PIPE)
        psql.communicate()


@cli.command('export')
@click.option("--output", "-o",
              type=click.Path(file_okay=False, exists=True),
              required=False, default=os.getcwd(), help='output destination')
@click.option("--driver", type=click.Choice(["shapefile", "csv", "tsv"]),
              default="shapefile", help='defaults to shapefile')
@click.option("--geometry-column", "-g",
              required=False, default='geom',
              help="specify geometry column")
@click.option("--wkt", required=False, is_flag=True,
              default=False, help="export geometry as wkt")
@click.argument("tables", nargs=-1, required=False)
def export_command(output, driver, geometry_column, wkt, tables):
    """Export PostGIS data"""
    print(f'--- export {driver} ---')
    output = os.path.abspath(output)
    available_tables = find_requested_tables(tables)
    for data_table in available_tables:
        print(f'>> {data_table}')
        has_geometry = is_geom_column(data_table, geometry_column)
        output = os.path.join(output, data_table + get_file_extension(driver))
        if driver == 'shapefile' and has_geometry:
            export_shapefile(data_table, output)
        elif driver == 'csv':
            export_csv(data_table, output, geometry_column, wkt, has_geometry, delimiter="','")
        elif driver == 'tsv':
            export_csv(data_table, output, geometry_column, wkt, has_geometry, delimiter="E'\t'")


@click.pass_obj
def is_geom_column(ctx, table, geometry_column):
    cur = ctx.conn.cursor()
    sql = f"""SELECT f_geometry_column FROM geometry_columns WHERE f_table_name = '{table}';"""
    cur.execute(sql)
    detected_geometries = [geo[0] for geo in cur.fetchall()]
    if geometry_column not in detected_geometries:
        return False
    return True


@click.pass_obj
def table_exists(ctx, table):
    cur = ctx.conn.cursor()
    sql = f"""SELECT * FROM information_schema.tables WHERE table_name='{table}'"""
    cur.execute(sql)
    return bool(cur.rowcount)


@click.pass_obj
def export_csv(ctx, table, output, geom_col, wkt, has_geom=True, delimiter=','):
    """Export PostGIS data to csv"""
    cur = ctx.conn.cursor()
    sql = f"""
          DROP TABLE IF EXISTS temp_export_table;
          SELECT * INTO temp_export_table FROM {table};"""
    cur.execute(sql)
    if has_geom:
        sql = f"""
            ALTER TABLE temp_export_table
               ADD COLUMN coordinate_y numeric,
               ADD COLUMN coordinate_x numeric;

            UPDATE temp_export_table SET
               coordinate_y = st_y(st_centroid(temp_export_table.{geom_col})),
               coordinate_x = st_x(st_centroid(temp_export_table.{geom_col}));"""
        cur.execute(sql)
        if wkt:
            sql = f"""
                ALTER TABLE temp_export_table ADD COLUMN wkt varchar;
                UPDATE temp_export_table SET wkt = st_astext(temp_export_table.{geom_col});"""
            cur.execute(sql)
        sql = f"""ALTER TABLE temp_export_table DROP COLUMN {geom_col};"""
        cur.execute(sql)
    else:
        print(f"geometry column '{geom_col}' not found")
    ctx.conn.commit()
    cmd = ['psql', '-h', ctx.host,
           '-d', ctx.dbname, '-U', ctx.user, '-p', ctx.port,
           '-c',  f"\\copy temp_export_table TO '{output}' DELIMITER {delimiter} CSV HEADER"]
    subprocess.run(cmd)
    sql = "DROP TABLE IF EXISTS temp_export_table;"
    cur.execute(sql)
    ctx.conn.commit()


@click.pass_obj
def export_shapefile(ctx, table, output):
    """Export PostGIS data to shapefile"""
    cmd = ['pgsql2shp', '-f', f'{output}', '-h', f'{ctx.host}',
           '-u', f'{ctx.user}', f'{ctx.dbname}', f'{ctx.schema}.{table}']
    subprocess.run(cmd, stderr=open(os.devnull, 'wb'))


@click.pass_obj
def get_data_tables(ctx):
    chill_tables = ['spatial_ref_sys']
    cur = ctx.conn.cursor()
    sql = f"""SELECT table_name
              FROM information_schema.tables
              WHERE table_schema='{ctx.schema}'
              AND table_type='BASE TABLE';"""
    cur.execute(sql)
    return [row[0] for row in cur.fetchall() if row[0] not in chill_tables]


def find_requested_tables(requested_tables):
    """Find user submitted database tables"""
    all_tables = get_data_tables()
    found_tables = []
    for t in requested_tables:
        if t in all_tables:
            found_tables.append(t)
        else:
            print(f'NOTICE:  table "{t}" does not exist')
    return found_tables


def get_file_extension(driver='shapefile'):
    """Return file extension for given driver"""
    drivers = {"shapefile": ".shp",
               "geodatabase": ".gdb",
               "geojson": ".geojson",
               "csv": ".csv",
               "tsv": ".tsv"}
    return drivers.get(driver)


def get_geo_files(directory, driver):
    """Find geo files for given directory"""
    file_extension = get_file_extension(driver)
    if os.path.isfile(directory):
        return [directory]
    geo_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                geo_files.append(os.path.join(root, file))
    return geo_files


if __name__ == '__main__':
    cli()
