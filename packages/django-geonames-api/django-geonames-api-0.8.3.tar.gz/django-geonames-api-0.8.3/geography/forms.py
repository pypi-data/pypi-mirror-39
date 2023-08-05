""" Geograpy forms
"""

# Django imports
from django.forms import ModelForm

# Models imports
from .models import City, Conurbation, Department, Region, Address

# Other imports
from dal import autocomplete


class CityForm(ModelForm):

    class Meta:
        model = City
        fields = '__all__'

        widgets = {
            'timezone': autocomplete.ModelSelect2(
                url='timezone-autocomplete',
            ),
            'conurbation': autocomplete.ModelSelect2(
                url='conurbation-autocomplete',
                forward=['department']
            ),
            'department': autocomplete.ModelSelect2(
                url='department-autocomplete',
                forward=['region']
            ),
            'region': autocomplete.ModelSelect2(
                url='region-autocomplete',
                forward=['country']
            ),
            'country': autocomplete.ModelSelect2(
                url='country-autocomplete',
            )
        }


class ConurbationForm(ModelForm):

    class Meta:
        model = Conurbation
        fields = '__all__'

        widgets = {
            'department': autocomplete.ModelSelect2(
                url='department-autocomplete',
                forward=['region']
            ),
            'region': autocomplete.ModelSelect2(
                url='region-autocomplete',
                forward=['country']
            ),
            'country': autocomplete.ModelSelect2(
                url='country-autocomplete',
            )
        }


class DepartmentForm(ModelForm):

    class Meta:
        model = Department
        fields = '__all__'

        widgets = {
            'region': autocomplete.ModelSelect2(
                url='region-autocomplete',
                forward=['country']
            ),
            'country': autocomplete.ModelSelect2(
                url='country-autocomplete',
            )
        }


class RegionForm(ModelForm):

    class Meta:
        model = Region
        fields = '__all__'

        widgets = {
            'country': autocomplete.ModelSelect2(
                url='country-autocomplete',
            )
        }


class AddressForm(ModelForm):

    class Meta:
        model = Address
        fields = '__all__'

        widgets = {
            'city': autocomplete.ModelSelect2(
                url='city-autocomplete'
            )
        }
