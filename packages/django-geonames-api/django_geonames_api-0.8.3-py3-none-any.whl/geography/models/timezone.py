# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import utc

# Datetime
from datetime import datetime
from pytz import timezone


class Timezone(models.Model):

    code2 = models.CharField(_('Country code 2'), max_length=2)
    name = models.CharField(
        _('Name'),
        max_length=50,
        blank=True,
        null=True
    )
    offset = models.DecimalField(
        _('Offset from GMT'),
        max_digits=3,
        decimal_places=1
    )

    def instance(self):
        return timezone(self.name)

    def get_datetime(self, dt=None):
        # get timezone
        tz = self.instance()

        if not dt:
            return datetime.now(tz)

        # return localized date
        return dt.astimezone(tz)

    def tzinfo_time(self, t):
        # create a timezone aware datetime from the given time
        dt = datetime.now(self.instance()).replace(
            hour=t.hour,
            minute=t.minute,
            second=0,
            microsecond=0
        )

        return dt.astimezone(self.instance())

    def localize_time(self, t):
        # create a timezone aware datetime from the given time
        dt = datetime.now(utc).replace(
            hour=t.hour,
            minute=t.minute,
            second=0,
            microsecond=0
        )

        return dt.astimezone(self.instance())

    def normalize_time(self, t):
        # create a timezone aware datetime from the given time
        dt = datetime.now(self.instance()).replace(
            hour=t.hour,
            minute=t.minute,
            second=0,
            microsecond=0
        )

        return dt.astimezone(utc)

    def __str__(self):
        return self.name
