# Django imports
from django.db.models import Q

# Models imports
from .models import City

# Other imports
from haystack.indexes import Indexable, LocationField, CharField,\
    IntegerField
from haystack.indexes import SearchIndex

from .string_utils import searchalize


class CityIndex(SearchIndex, Indexable):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name', faceted=True)
    code = CharField(model_attr='code')
    location_city = LocationField(model_attr='get_location')
    namelength = IntegerField(model_attr='get_name_length')

    def get_model(self):
        return City

    def index_queryset(self, using=None):
        r"""Used when the entire index for model is updated."""
        queryset = super(CityIndex, self).index_queryset(using)
        return queryset.exclude(
            Q(code__contains="CEDEX") |
            Q(code__contains="SP"))

    def prepare_name(self, obj):
        return searchalize(self.prepared_data['name'])
