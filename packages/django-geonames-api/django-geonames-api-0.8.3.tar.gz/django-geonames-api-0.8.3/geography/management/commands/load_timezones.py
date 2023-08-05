# -*- coding: utf-8 -*-
r""" Command to load timezones from geonames' timeZones.txt
"""

# Django imports
from django.core.management.base import BaseCommand, CommandError
from geography.models import Timezone, City, Country

# Python imports
from urllib.request import urlopen


class Command(BaseCommand):

    default_url = 'http://download.geonames.org/export/dump/timeZones.txt'

    args = '[url|file]'
    help = 'Load timezones from "{}" by default\n' \
           'or from the given url or file.'.format(default_url)

    def handle(self, *args, **options):
        r""" Handle the command to load timezone informations
        """

        try:
            # Open file
            if len(args) == 1:
                try:
                    # From file
                    f = open(args[0], 'r')
                except IOError:
                    # From URL given as parameter
                    f = urlopen(args[0])
            else:
                # From default URL
                f = urlopen(self.default_url)
        except ValueError:
            raise CommandError('Couldn\'t load the file.')

        # Parse file
        self.stdout.write('Loading timezones...')
        self.load_timezones(f)

        # Update cities
        self.stdout.write('Updating cities...')
        self.update_cities()

    def load_timezones(self, file_obj):
        # Load into database
        processed_counter = 0
        updated_counter = 0
        for line in file_obj:
            elem = str(line.decode("utf-8")).split("\t", 3)
            try:
                updated_values = {
                    'code2': elem[0],
                    'name': elem[1],
                    'offset': elem[2]
                }
                is_updated = False

                try:
                    obj = Timezone.objects.get(name=elem[1])

                    for key, value in updated_values.items():
                        setattr(obj, key, value)
                    obj.save()
                    is_updated = True
                except Timezone.DoesNotExist:
                    obj = Timezone(**updated_values)
                    obj.save()

                processed_counter += 1
                if is_updated:
                    updated_counter += 1
            except Exception as e:
                print(str(e) + " | " + str(line))

        print(
            "Processed {} timezones ({} updated).".format(
                processed_counter,
                updated_counter
            )
        )

    def update_cities(self):
        # get timezone
        prompt = '> '

        for pays in Country.objects.all():
            try:
                try:
                    tz = Timezone.objects.get(code2=pays.code2)
                except Timezone.MultipleObjectsReturned:
                    while True:
                        tzs = Timezone.objects.filter(code2=pays.code2)
                        print("------")
                        print("[" + pays.code2 + "]")
                        for tzn in tzs:
                            print("-> " + str(tzn.id) + " " + tzn.name)

                        tzgood = input(prompt)
                        if int(tzgood) == -1:
                            raise Timezone.MultipleObjectsReturned
                        else:
                            try:
                                tz = Timezone.objects.get(code2=pays.code2,
                                                          id=int(tzgood))
                                break
                            except Exception:
                                pass

                for city in City.objects.select_related('timezone')\
                        .filter(country__code2=pays.code2):
                    if(city.timezone != tz or not city.timezone):
                        city.timezone = tz
                        city.save()
                        print(
                            "Updated city '{}' -> {}".format(city.id, tz.name)
                        )

            except (Timezone.DoesNotExist, Timezone.MultipleObjectsReturned):
                pass
