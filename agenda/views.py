import os
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime
from models import Stamp, DayStamp


def jsonable_stamps():
    stamps = {}
    for stamp in Stamp.objects.all():
        stamps[stamp.id] = {
            'id': stamp.id,
            'img': os.path.join('static/', stamp.path),
            'name': stamp.name,
        }
    return stamps


def streak(request):
    return JsonResponse({'foo': 'bar'})


def index(request):
    return render(request, 'index.html')


def month(request, year, month):
    year = int(year)
    month = int(month)
    stamped = {}
    for ds in DayStamp.month_query(year, month).all():
        key = '{0.year}-{0.month}-{0.day}'.format(ds.date)
        if key not in stamped:
            stamped[key] = []
        stamped[key].append(ds.stamp_id)

    return JsonResponse({
        'date': datetime(year, month, 1).isoformat(),
        'stamps': jsonable_stamps(),
        'stamped': stamped,
    })
