# Django imports
from django.test import TestCase

# External imports
from model_mommy import mommy


class TestAddressStr(TestCase):

    @classmethod
    def setUpTestData(cls):
        country = mommy.make('geography.Country', name='FRANCE')
        cls.city = mommy.make(
            'geography.City',
            name='Saint-Herblain',
            code='44800',
            country=country
        )

    def test_with_full_address(self):
        address = mommy.make(
            'geography.Address',
            number='15',
            street='avenue Marcelin Berthelot',
            complement='Atalante 1 - Bât. C',
            city=self.city
        )
        expected_address = (
            "15 avenue Marcelin Berthelot, Atalante 1 - Bât. C "
            "44800 Saint-Herblain, FRANCE"
        )
        assert str(address) == expected_address

    def test_with_missing_number(self):
        address = mommy.make(
            'geography.Address',
            street='avenue Marcelin Berthelot',
            complement='Atalante 1 - Bât. C',
            city=self.city
        )
        expected_address = (
            "avenue Marcelin Berthelot, Atalante 1 - Bât. C "
            "44800 Saint-Herblain, FRANCE"
        )
        assert str(address) == expected_address

    def test_without_address_complement(self):
        address = mommy.make(
            'geography.Address',
            number='15',
            street='avenue Marcelin Berthelot',
            city=self.city
        )
        expected_address = (
            "15 avenue Marcelin Berthelot 44800 Saint-Herblain, FRANCE"
        )
        assert str(address) == expected_address

    def test_without_first_line_address(self):
        address = mommy.make(
            'geography.Address',
            city=self.city
        )
        expected_address = " 44800 Saint-Herblain, FRANCE"

        assert str(address) == expected_address

    def test_completeStreetName_withtoutComplement_returnStreetName(self):
        street_name = 'avenue Marcelin Berthelot'
        address = mommy.make(
            'geography.Address',
            street=street_name
        )

        assert address.complete_street_name() == street_name

    def test_completeStreetName_withComplement_returnStreetNameWithComplement(self):
        address = mommy.make(
            'geography.Address',
            street='avenue Marcelin',
            complement='Berthelot'
        )

        assert address.complete_street_name() == 'avenue Marcelin Berthelot'
