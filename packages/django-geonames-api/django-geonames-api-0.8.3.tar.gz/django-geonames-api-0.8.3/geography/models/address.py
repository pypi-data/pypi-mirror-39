# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Address(models.Model):

    class Meta:
        verbose_name = 'Adresse'

    number = models.CharField(_('numéro'), max_length=5, blank=True, null=True)
    street = models.CharField(_('rue'), max_length=250, blank=True, null=True)
    complement = models.CharField(
        _("complément d'adresse"),
        max_length=250,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        'geography.City',
        verbose_name=_('city'),
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def complete_street_name(self):
        if self.complement:
            return " ".join([self.street, self.complement])

        return self.street

    def __str__(self):
        number = self.number
        street = self.street
        complement = self.complement
        city = self.city

        address = ""

        if number:
            address += number + " "
        if street:
            address += street
        if complement:
            address += ", " + complement

        if city:
            city_name = self.city.name
            code = self.city.code
            country = self.city.country.name

            city_infos = " {code} {city}, {country}".format(
                code=code,
                city=city_name,
                country=country
            )
            address += city_infos

        return address

    class Meta:
        verbose_name_plural = "addresses"