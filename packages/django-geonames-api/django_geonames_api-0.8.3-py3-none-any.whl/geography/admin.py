r""" Geography administration
"""

# Django imports
from django.contrib import admin

# Models imports
from .models import (
    Timezone, Country, Region, Department, Conurbation, City, Address
)

# Form imports
from .forms import (
    CityForm, ConurbationForm, DepartmentForm, RegionForm, AddressForm
)


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country')
    search_fields = ['name', 'code']
    form = CityForm

    def country(self, obj):
        return obj.country.name


class ConurbationAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'region', 'country')
    search_fields = ['name']
    form = ConurbationForm


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'country')
    search_fields = ['name']
    form = DepartmentForm


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ['name']
    form = RegionForm


class AddresseAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'street',
        'complement',
        'city'
    )
    search_fields = ['city']
    form = AddressForm


admin.site.register(Timezone)
admin.site.register(Country)
admin.site.register(Region, RegionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Conurbation, ConurbationAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddresseAdmin)
