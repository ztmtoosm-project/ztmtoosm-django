from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.template import loader
from django.db.models import Q
from django.http import JsonResponse
import json
import functools
import re
import json
from MySuperApp.views import sort1


def index11(request):
    q = ScheduleTmp.objects.filter(line=request.GET['line'], stop_id=request.GET['id'], day_type='DP').order_by('time_seconds')
    alfa = dict()
    for x in range(0, 40):
        alfa[x] = []
    for x in q:
        alfa[int((x.time_seconds)/3600)].append(int(x.time_seconds/60)%60)
    print(alfa)
    template = loader.get_template('pools/index7.html')

    return HttpResponse(template.render({'abc' : alfa}, request))
