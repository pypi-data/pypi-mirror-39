r""" User autocomplete
"""

# Moills imports
from django.db.models import Q

from .models import (
    Address,
    City,
    Conurbation,
    Department,
    Region,
    Country,
    Timezone
)

# Other imports
from dal import autocomplete


class AddressAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Address.objects.select_related('city').all()

        if self.q:
            qs = qs.filter(
                Q(street__icontains=self.q)
                | Q(complement__icontains=self.q)
                | Q(city__name__icontains=self.q)
            )

        return qs


class TimezoneAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Timezone.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = City.objects.all()

        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)

        region = self.forwarded.get('region', None)
        if region:
            qs = qs.filter(region=region)

        department = self.forwarded.get('department', None)
        if department:
            qs = qs.filter(department=department)

        conurbation = self.forwarded.get('conurbation', None)
        if conurbation:
            qs = qs.filter(conurbation=conurbation)

        if self.q:
            qs = qs.filter(
                Q(name__icontains=self.q) |
                Q(code__istartswith=self.q)
            )

        return qs


class ConurbationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Conurbation.objects.all()

        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)

        region = self.forwarded.get('region', None)
        if region:
            qs = qs.filter(region=region)

        department = self.forwarded.get('department', None)
        if department:
            qs = qs.filter(department=department)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class DepartmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Department.objects.all()

        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)

        region = self.forwarded.get('region', None)
        if region:
            qs = qs.filter(region=region)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class RegionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Region.objects.all()

        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Country.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
