import calendar
from django.conf import settings
from django.db import models
from datetime import datetime


class Stamp(models.Model):
    name = models.CharField(max_length=64, unique=True)
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return '{0}: \'{1}\''.format(self.name, self.path)

    def __repr__(self):
        return '<Stamp %r>' % self.name


class DayStamp(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    date = models.DateField()
    stamp = models.ForeignKey(Stamp)

    class Meta:
        unique_together = ('date', 'stamp')

    @classmethod
    def create(cls, user, date, stamp):
        ds = cls()
        ds.user = user
        ds.date = date
        ds.stamp = stamp
        return ds

    def __str__(self):
        return '{2} ({1}) by {0}'.format(self.user.username, self.date, self.stamp.name)

    def __repr__(self):
        return '<DayStamp %r %r %r>' % (self.user.username, self.date, self.stamp.name)

    @staticmethod
    def month_query(user, year, month):
        """
        gets a query which will return all DayStamps within the provided month
        returns a query as it can be used to both retrieve or delete
        """
        first = datetime(year, month, 1)
        last = datetime(year, month, calendar.monthrange(year, month)[1])
        return DayStamp.objects.filter(user=user, date__range=(first, last))

    @staticmethod
    def current_streak(user, upto=None):
        """
        gets the current streak back from the provided date (default today)
        """
        if upto is None:
            upto = datetime.today().date()
        all_ds = DayStamp.objects.filter(user=user, date__lte=upto).order_by('-date')

        current = []
        last = None
        for ds in all_ds:
            if last is None and (ds.date - upto).days <= 1:
                last = ds
                current.append(ds)
                continue
            if (last.date - ds.date).days <= 1:
                current.append(ds)
            else:
                break
            last = ds

        current.reverse()
        return current
