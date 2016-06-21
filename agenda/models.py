import calendar
from django.db import models
from datetime import datetime


class Stamp(models.Model):
    name = models.CharField(max_length=64, unique=True)
    path = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return '<Stamp %r>' % self.name

    def __repr__(self):
        return '<Stamp %r>' % self.name


class DayStamp(models.Model):
    date = models.DateField()
    stamp = models.ForeignKey(Stamp)

    class Meta:
        unique_together = ('date', 'stamp')

    @classmethod
    def create(cls, date, stamp):
        ds = cls()
        ds.date = date
        ds.stamp = stamp
        return ds

    def __str__(self):
        return '<DayStamp %r %r>' % (self.date, self.stamp.name)

    def __repr__(self):
        return '<DayStamp %r %r>' % (self.date, self.stamp.name)

    @staticmethod
    def month_query(year, month):
        """
        gets a query which will return all DayStamps within the provided month
        returns a query as it can be used to both retrieve or delete
        """
        first = datetime(year, month, 1)
        last = datetime(year, month, calendar.monthrange(year, month)[1])
        return DayStamp.objects.filter(date__range=(first, last))

    @staticmethod
    def current_streak(upto=None):
        """
        gets the current streak back from the provided date (default today)
        """
        if upto is None:
            upto = datetime.today()
        all_ds = DayStamp.query         \
            .filter(DayStamp.date < upto)   \
            .order_by(DayStamp.date.desc()) \
            .all()

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
