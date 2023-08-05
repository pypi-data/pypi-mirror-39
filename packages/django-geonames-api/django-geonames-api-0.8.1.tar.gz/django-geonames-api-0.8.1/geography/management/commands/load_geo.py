# -*- coding: utf-8 -*-

r""" Command to load geographic information from internet or local file.
"""


# Built-in imports
import csv
from io import BytesIO, StringIO
from os.path import basename, splitext
from urllib.request import urlopen
from zipfile import ZipFile

# Django imports
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import F, Func, Value

# Models imports
from geography.models import (
    Conurbation, Department, Country, Region, Timezone, City,
)


class Command(BaseCommand):
    """
    Command to load Geonames format CSV file into the geographic tables
    of the database. Geonames format CSV file can either be loaded directly
    from the website or from a local file.
    """

    geonames_csv_url = 'http://download.geonames.org/export/zip/FR.zip'
    args = 'geo_csv'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delimiter',
            '-d',
            dest='delimiter',
            default='\t',
            help='CSV fields delimiter'
        )
        parser.add_argument(
            '--country',
            '-c',
            dest='country',
            default='FR',
            help='Country code2'
        )
        parser.add_argument(
            'url',
            nargs='?',
            type=str,
            default=self.geonames_csv_url,
            help='Geonames URL'
        )

    help = (
        'Load geographic data with geonames format CSV file. '
        'Download example at ' + geonames_csv_url + '.'
        'With CSV path, the tool will load the CSV. Without, it will '
        'download the ZIP directly from geonames website and get the'
        'text file with the same name from it.\n'
        'For example, from FR.zip file, the tool will try to read'
        'the file FR.txt'
    )

    @staticmethod
    def get_csv_from_url(url):
        """
        Get zipped CSV from specified URL and extract the text file which
        has the same name as the ZIP.
        """
        url_descriptor = urlopen(url)
        filename = splitext(basename(url))[0] + '.txt'
        return ZipFile(BytesIO(url_descriptor.read())).open(filename)

    @staticmethod
    def parse_csv_line(line):
        """
        Parse a CSV line and return the corresponding city information in
        a dictionnary.

        Array fields ( http://download.geonames.org/export/zip/readme.txt ) :

        country code : iso country code, 2 characters
        postal code  : varchar(20)
        place name   : varchar(180)
        admin name1  : 1. order subdivision (state) varchar(100)
        admin code1  : 1. order subdivision (state) varchar(20)
        admin name2  : 2. order subdivision (county/province) varchar(100)
        admin code2  : 2. order subdivision (county/province) varchar(20)
        admin name3  : 3. order subdivision (community) varchar(100)
        admin code3  : 3. order subdivision (community) varchar(20)
        latitude     : estimated latitude (wgs84)
        longitude    : estimated longitude (wgs84)
        accuracy     : accuracy of lat/lng from 1=estimated to 6=centroid
        """

        city_information = {
            'country': {'code': line[0]},
            'state': {
                'code': line[4],
                'name': line[3]
            },
            'county': {
                'code': line[6],
                'name': line[5]
            },
            'community': {
                'code': line[8],
                'name': line[7],
            },
            'city': {
                'postcode': line[1],
                'name': line[2],
                'latitude': line[9],
                'longitude': line[10],
                'accuracy': line[11]
            }
        }

        return city_information

    @classmethod
    def load_state(cls, country, state):
        """Save and return state."""
        # Variable initialization
        reg = None

        # Load state
        if(state['code'] != '' and state['name'] != ''):
            reg = Region.objects.update_or_create(**{
                'name': state['name'],
                'country': country
            }, defaults={
                'code': state['code']
            })[0]

        return reg

    @classmethod
    def load_county(cls, country, state, county):
        """Save and return county."""
        # Variable initialization
        dep = None

        # Load county
        if(county['code'] != '' and county['name'] != ''):
            dep = Department.objects.update_or_create(**{
                'name': county['name'],
                'country': country,
            }, defaults={
                'code': county['code'],
                'region': state
            })[0]

        return dep

    @classmethod
    def load_community(cls, country, state, county, community):
        """Save and return community."""
        # Variable initialization
        agg = None

        # Load community
        if(community['code'] != '' and community['name'] != ''):
            agg = Conurbation.objects.update_or_create(
                department=county,
                name=community['name'],
                country=country,
                defaults={
                    'code': community['code'],
                    'region': state
                }
            )[0]

        return agg

    def clean_models_quotes(self, model):
        self.stdout.write(
            str(
                model.objects.filter(name__icontains='’').update(
                    name=Func(
                        F('name'),
                        Value('’'), Value('\''),
                        function='replace',
                    )
                )
            ),
            ending="\n"
        )

    def save_city_information(self, city_information):
        """Save city information in the database."""

        def printupdate(v, valtype, newval):
            self.stdout.write(
                "update %s (%s) %s %s to %s" % (
                    v.name,
                    v.code,
                    valtype,
                    getattr(v, valtype),
                    newval
                ),
                ending="\n"
            )

        def replace_quotes(v):
            return str(v).replace('’', '\'')

        def updatecity(v, city_information, agg, dep, reg, pys):
            # Load place
            changes = False
            if replace_quotes(v.conurbation) != replace_quotes(agg):
                printupdate(v, "conurbation", agg)
                v.conurbation = agg
                changes = True

            if replace_quotes(v.department) != replace_quotes(dep):
                printupdate(v, "department", dep)
                v.department = dep
                changes = True

            if replace_quotes(v.region) != replace_quotes(reg):
                printupdate(v, "region", reg)
                v.region = reg
                changes = True

            if replace_quotes(v.country) != replace_quotes(pys):
                printupdate(v, "country", pys)
                v.country = pys
                changes = True

            # update timezone
            if not v.timezone:
                tz = Timezone.objects.get(
                    code2=city_information['country']['code']
                )
                v.timezone = tz
                changes = True

            if changes:
                v.save()

        # Load country
        pys, __ = Country.objects.get_or_create(
            code2=city_information['country']['code']
        )
        reg = self.load_state(pys, city_information['state'])
        dep = self.load_county(pys, reg, city_information['county'])
        conu = self.load_community(pys, reg, dep, city_information['community'])
        city = city_information['city']

        try:
            v = City.objects.get(
                code=city['postcode'],
                name=city['name']
            )
            updatecity(v, city_information, conu, dep, reg, pys)
        except MultipleObjectsReturned:
            vs = City.objects.filter(
                code=city['postcode'],
                name=city['name']
            )
            for v in vs:
                self.stdout.write(
                    "%s : dup %d" % (city['name'], v.id),
                    ending="\n"
                )
                updatecity(v, city_information, conu, dep, reg, pys)
        except City.DoesNotExist:
            City.objects.create(
                conurbation=conu,
                code=city['postcode'],
                department=dep,
                latitude=city['latitude'],
                longitude=city['longitude'],
                name=city['name'],
                country=pys,
                precision=city['accuracy'],
                region=reg,
                timezone=Timezone.objects.get(
                    code2=city_information['country']['code']
                )
            )

    def handle(self, *args, **options):
        """Handle the command to load geographical information."""

        # Open CSV
        if len(args) == 1:
            try:
                # From file
                csvfile = open(options['url'], 'rb')
            except IOError:
                # From URL given as parameter
                csvfile = self.get_csv_from_url(options['url'])
        else:
            # From default URL
            csvfile = self.get_csv_from_url(self.geonames_csv_url)

        # Cleaning quotes to avoid missmatches
        selected_country = Country.objects.get(code2=options['country'])
        self.stdout.write(
            str(City.objects.filter(country=selected_country).count()),
            ending="\n"
        )

        # Read CSV
        city_file = csv.reader(
            StringIO(csvfile.read().decode('UTF-8')),
            delimiter=options['delimiter']
        )

        # Cleaning quotes to avoid missmatches
        for model in [City, Conurbation, Region, Country]:
            self.stdout.write(str(model), ending="\n")
            self.clean_models_quotes(model)

        # Save all cities
        for line in city_file:
            city_information = self.parse_csv_line(line)
            self.save_city_information(city_information)
