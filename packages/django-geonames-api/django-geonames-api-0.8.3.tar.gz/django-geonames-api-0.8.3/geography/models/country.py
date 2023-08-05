# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):

    name = models.CharField(
        _('Country name'),
        max_length=100,
        blank=True,
        null=True
    )
    code2 = models.CharField(_('Country code 2'), max_length=2)
    code3 = models.CharField(
        _('Country code 3'),
        max_length=3,
        blank=True,
        null=True
    )
    number = models.CharField(
        _('Country number'),
        max_length=3,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "countries"
