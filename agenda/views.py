import os
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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


@login_required
def streak(request):
    return JsonResponse({'foo': 'bar'})


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
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


@login_required
def save(request):
    date = request.POST['date']
    tokens = date.split('-')
    date = datetime(int(tokens[0]), int(tokens[1]), int(tokens[2]))
    stamp = Stamp.objects.get(id=int(request.POST['stamp']))
    addStamp = request.POST['addStamp']

    if addStamp.lower() in ['true', '1']:
        ds = DayStamp.create(date, stamp)
        ds.save()
    else:
        ds = DayStamp.objects.get(date=date, stamp=stamp)
        ds.delete()
    return JsonResponse({})
