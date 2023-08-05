import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.rst").read_text()


setup(
    name='postgis-toolkit',
    version='0.0.1',
    description='PostGIS Commands',
    long_description=README,
    url='https://github.com/felixink/postgis-toolkit',
    author='Felix Rhett',
    author_email='felix.rhett@gmail.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=['postgis', 'postgres', 'gis', 'shapefile', 'pgsql2shp'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7*',
    install_requires=[
        'Click',
        'psycopg2-binary',
        'tabulate'
    ],
    entry_points={
        "console_scripts": [
            "pgtk=pgtk.pgtk:cli",
        ]
    },
)
