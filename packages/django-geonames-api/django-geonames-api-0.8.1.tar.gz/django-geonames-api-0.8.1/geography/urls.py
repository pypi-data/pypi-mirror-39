# Django imports
from django.conf.urls import url

# Autocomplete imports
from .autocomplete import (
    AddressAutocomplete, CityAutocomplete, ConurbationAutocomplete,
    DepartmentAutocomplete, RegionAutocomplete, CountryAutocomplete,
    TimezoneAutocomplete
)
from django.urls import include
from .api import CityResource

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(CityResource())

urlpatterns = [

    url(r'^api/', include(v1_api.urls)),

    # Autocomplete
    url(r'^address-autocomplete/$', AddressAutocomplete.as_view(),
        name='address-autocomplete'),

    url(r'^city-autocomplete/$', CityAutocomplete.as_view(),
        name='city-autocomplete'),

    url(r'^conurbation-autocomplete/$', ConurbationAutocomplete.as_view(),
        name='conurbation-autocomplete'),

    url(r'^department-autocomplete/$', DepartmentAutocomplete.as_view(),
        name='department-autocomplete'),

    url(r'^region-autocomplete/$', RegionAutocomplete.as_view(),
        name='region-autocomplete'),

    url(r'^country-autocomplete/$', CountryAutocomplete.as_view(),
        name='country-autocomplete'),

    url(r'^timezone-autocomplete/$', TimezoneAutocomplete.as_view(),
        name='timezone-autocomplete'),
]
