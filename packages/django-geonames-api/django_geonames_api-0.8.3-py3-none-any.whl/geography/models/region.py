# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Region(models.Model):

    country = models.ForeignKey('geography.Country', on_delete=models.PROTECT)
    name = models.CharField(_('State name'), max_length=100)
    code = models.CharField(_('State code'), max_length=20)

    def __str__(self):
        return self.name
