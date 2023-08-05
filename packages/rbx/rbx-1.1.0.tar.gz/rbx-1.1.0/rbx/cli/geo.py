#!/usr/bin/env python
"""The script extracts the data from the various database files, and generates a series of files
that the Rig UI can use.

The database is the MaxMind GeoIP2 CSV Databases (City and Country).
See https://dev.maxmind.com/geoip/geoip2/geoip2-city-country-csv-databases/
"""
import csv
import json
import sqlite3
import shutil
from os import path, makedirs, remove

import click

from rbx.ext.maps.client import Client


def clean(value):
    """Strip trailing whitespaces and quotes."""
    return value.strip(' "')


def create_database(labels, db):
    """Create a sqlite3 database using the list of labels."""
    if path.exists(db):
        remove(db)

    with sqlite3.connect(db) as conn:
        c = conn.cursor()

        c.execute('CREATE TABLE labels (country text, label text, region text)')

        c.executemany(
            'INSERT INTO labels (country, label, region) VALUES (?, ?, ?)',
            [(label['country'], label['label'], label['region']) for label in labels]
        )

        conn.commit()


class Packer:
    """The base GeoIP Packer."""
    def __init__(self, db_path, data_dir):
        """The version of the db is inferred from the path to the folder. As that path should
        always be a versioned path. e.g.: ./data/<version>/
        """
        self.db_path = path.normpath(db_path)
        self.data_dir = data_dir
        self.version = path.split(self.db_path)[-1]
        self.data_dir = path.join(path.normpath(data_dir), self.version)

        # This will hold the final JSON payload
        self.countries = {}

    def __call__(self):
        self.claim_version()

        try:
            self.read_countries()
            self.read_regions()
            self.read_cities()
        except (FileNotFoundError, TypeError):
            raise SystemExit

        # Wipe out the destination folder.
        if path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        makedirs(path.join(self.data_dir, 'countries'))

        # The area labels are stored in a sqlite3 database.
        labels = []

        # Output country list (geo.json)
        # ------------------------------
        # Format:
        #   {
        #     "categories": [
        #       {
        #         "sub": [
        #           {
        #             "value": "<country_code>",
        #             "label": "<country_name>"
        #           },
        #           ...
        #         ],
        #         "label": "<country_name>[:1]",
        #         "value": "<country_name>[:1]"
        #       },
        #       ...
        #     ]
        #   }
        #
        output = {
            'categories': [
                {
                    'sub': {'label': code, 'value': value['name']},
                    'label': value['name'][:1],
                    'value': value['name'][:1],
                }
                for code, value in sorted(self.countries.items())
            ]
        }
        with open(path.join(self.data_dir, 'geo.json'), mode='w', encoding='utf-8') as fd:
            fd.write(json.dumps(output, indent=2))

        # Create country files (countries/<country_code>.json)
        # ------------------------------
        # Format:
        #   {
        #     "categories": [
        #       {
        #         "country": "<country_code>",
        #         "value": "<region_code>",
        #         "label": "<region_name>",
        #         "sub": [
        #           {
        #             "value": "<city>",
        #             "label": "<city>"
        #           },
        #           ...
        #         ]
        #       },
        #       ...
        #     ]
        #   }
        #
        for country_code, country in self.countries.items():
            output = {
                'categories': [
                    {
                        'country': country_code,
                        'label': region['name'],
                        'value': code,
                        'sub': [
                            {
                                'label': city,
                                'value': city
                            }
                            for city in sorted(region['cities'])
                        ],
                    }
                    for code, region in sorted(country['regions'].items())
                ]
            }

            # Add each region to the list of labels.
            # Ignore the 'Unspecified Region' labels.
            for code, region in sorted(country['regions'].items()):
                if code == 'N/A':
                    continue

                labels.append({'country': country_code, 'label': region['name'], 'region': code})

            country_file = path.join(self.data_dir, 'countries', country_code + '.json')
            with open(country_file, mode='w', encoding='utf-8') as fd:
                fd.write(json.dumps(output))

        db = path.join(self.data_dir, 'area.db')
        click.echo('Creating area database "{}".'.format(db))
        create_database(labels, db)

        click.echo('\U0001F44D Done.')
        click.echo('Now run "aws s3 sync {} s3://<bucket>/rig/geo/{}" to upload to S3.'.format(
            self.data_dir, self.version))

    def claim_version(self):
        raise NotImplementedError

    def read_cities(self):
        raise NotImplementedError

    def read_countries(self):
        raise NotImplementedError

    def read_regions(self):
        raise NotImplementedError


class GeoIP2Packer(Packer):
    encoding = 'utf-8'

    def claim_version(self):
        """Display the GeoIP version used."""
        click.echo('Unpacking GeoIP2 DB "{}" to "{}" folder.'.format(self.version, self.data_dir))

    def read_cities(self):
        """Read the region and city from the 'GeoIP2-City.csv' file."""
        with open(path.join(self.db_path, 'GeoIP2-City.csv'), encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                # Skip entries with no city.
                if not row['city_name']:
                    continue

                # Case 1: both sub-divisions are present; the region code is compiled from both
                # codes, separated by a dot (i.e.: '<sd1_code>.<sd2_code>'); the second division
                # name is used as the region name, with the first division in brackets.
                if row['subdivision_1_iso_code'] and row['subdivision_2_iso_code']:
                    region_code = '{}.{}'.format(
                        row['subdivision_1_iso_code'], row['subdivision_2_iso_code'])
                    region_name = '{} ({})'.format(
                        row['subdivision_2_name'], row['subdivision_1_name'])

                # Case 2: only the first sub-division is filled in; we just use that for region
                # code and name.
                elif row['subdivision_1_iso_code']:
                    region_code = row['subdivision_1_iso_code']
                    region_name = row['subdivision_1_name']

                # Case 3: no sub-divisions at all. We create a dummy 'Unspecified Region' region
                # with code 'N/A'.
                else:
                    region_code = 'N/A'
                    region_name = 'Unspecified Region'

                if region_code not in self.countries[row['country_iso_code']]['regions']:
                    self.countries[row['country_iso_code']]['regions'][region_code] = {
                        'name': region_name,
                        'cities': set([row['city_name']]),
                    }
                else:
                    self.countries[row['country_iso_code']]['regions'][
                        region_code
                    ]['cities'].add(row['city_name'])

    def read_countries(self):
        """Read the country code and name from the 'GeoIP2-Country.csv' file."""
        with open(path.join(self.db_path, 'GeoIP2-Country.csv'), encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                country = clean(row['country_iso_code'])
                if country:
                    self.countries[country] = {
                        'name': clean(row['country_name']),
                        'regions': {},
                    }

    def read_regions(self):
        """The regions are part of the City file, so there's nothing to do here."""


@click.command(help='Unpack the GeoIP databases from the DB_PATH folder.')
@click.argument('db_path')
@click.option('-d', '--data-dir', default='geo-data',
              help='Destination folder for the extracted data (defaults to "./geo-data").')
def unpack(db_path, data_dir):
    packer = GeoIP2Packer(db_path, data_dir)

    try:
        packer()
    except SystemExit:
        click.echo('Cannot find the database files.')


@click.command(help='Fetch the Geocode for the given location.')
@click.argument('location')
@click.option('-c', '--country', help='Optional country code.')
@click.option('--key', help='google Cloud API key.', required=True)
def geocode(location, country=None, key=None):
    client = Client(key=key)
    geocode = client.geocode(location, country)

    if geocode is None:
        click.echo("Maps can't find '{}'".format(location))

    else:
        click.echo(click.style(geocode.location, fg='green'))
        click.echo('Precision: {0.name} ({0.value})'.format(geocode.location_type))
        click.echo(click.style(' > SW: {}'.format(geocode.viewport.southwest), bold=True))
        click.echo(click.style(' > NE: {}'.format(geocode.viewport.northeast), bold=True))
