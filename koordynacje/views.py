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


def index2(request):
    q = OperatorRoutes.objects.values('route_id').distinct()
    q2 = [{'lin' : x['route_id']} for x in q]
    q2 = sorted(q2, key=sort1)
    q3 = [x['lin'] for x in q2]
    return HttpResponse(json.dumps(q3, ensure_ascii=False), content_type="application/json; encoding=utf-8")

def index3(request, lin):
    q = LineDirections.objects.filter(line=lin).order_by('trip', 'id2')
    dtc = dict()
    for x in q:
        if x.trip not in dtc:
            dtc[x.trip] = []
        dtc[x.trip].append(x.name)
    dtc2 = dict()
    for p in dtc:
        dtc2[p] = dtc[p][0] + " > " + dtc[p][len(dtc[p])-1]
    return HttpResponse(json.dumps(dtc2, ensure_ascii=False), content_type="application/json; encoding=utf-8")

def all_line_stops(request, lin):
    q = OperatorRoutes.objects.filter(route_id=lin).order_by('direction', 'stop_on_direction_number')
    q2 = set()
    for x in q:
        q2.add(x.stop_id)
    q3 = OperatorStops.objects.filter(stop_id__in=q2)
    q4 = dict()
    for x in q3:
        q4[x.stop_id] = x.name
    ans = []
    for z in q:
        if z.stop_id in q4:
            ans.append({'stop_id' : z.stop_id, 'name' : q4[z.stop_id]})
    return HttpResponse(json.dumps(ans, ensure_ascii=False), content_type="application/json; encoding=utf-8")

def dfs(current, visited, level, levels, graph):
    if current in visited:
        return level
    visited.add(current)
    if current in graph:
        for k in graph[current]:
            level = dfs(k, visited, level, levels, graph)
    level = level+1
    levels[current] = level
    return level

def dfs_init(semi_graph):
    level = 0
    visited = set()
    levels = dict()
    extras = set()
    graph = dict()
    graph2 = dict()
    for p in semi_graph:
        if p[0] not in graph:
            graph[p[0]] = set()
        graph[p[0]].add(p[1])
    for p in semi_graph:
        if p[1] not in graph2:
            graph2[p[1]] = set()
        graph2[p[1]].add(p[0])
    for p in graph:
        level = dfs(p, visited, level, levels, graph)
    for p in graph:
        if len(graph[p]) > 1:
            extras.add(p)
    for p in graph2:
        if len(graph2[p]) > 1:
            extras.add(p)
    return (levels, extras)

def get_real_time(tim):
    tim = int(tim/60)
    hours = int(tim/60)
    minutes = tim%60
    minutes2 = str(minutes)
    if(minutes<10):
        minutes2 = "0"+minutes2
    return str(hours) + ":" + minutes2

@csrf_exempt
def index4(request):
    kpk = json.loads(request.POST['trips'])
    kpk2 = [x[0] for x in kpk]
    kpk3 = {(x[0], int(x[2])) for x in kpk}
    ptt = OperatorRoutes.objects.filter(route_id__in=kpk2).order_by('route_id', 'direction', 'stop_on_direction_number')
    ptt2 = dict()
    consider_stops = set()
    for z in ptt:
        if ((z.route_id, z.direction) in kpk3):
            if (z.route_id, z.direction) not in ptt2:
                ptt2[(z.route_id, z.direction)] = []
            ptt2[(z.route_id, z.direction)].append(z.stop_id)
            consider_stops.add(z.stop_id)
    ptt3 = set()
    for z in ptt2:
        for i in range(0, len(ptt2[z])-1):
            ptt3.add((ptt2[z][i], ptt2[z][i+1]))
    krotki = tuple(ptt3)
    res9 = ScheduleTmp.objects.raw("SELECT * FROM schedule WHERE trip IN (SELECT DISTINCT s1.trip FROM schedule s1, schedule s2 WHERE s1.day_type='DP' AND s1.trip=s2.trip AND s1.next_stop_trip+1 = s2.next_stop_trip+1 AND (s1.stop_id, s2.stop_id) IN %s AND s1.line IN %s)", [krotki, tuple(kpk2)])
    pt = dict()
    pt_bis = dict()
    for alfa in consider_stops:
        pt_bis[alfa] = set()
    for x in res9:
        if x.trip not in pt:
            pt[x.trip] = dict()
            pt[x.trip]['line_id'] = x.line
        pt[x.trip][x.stop_id] = x.time_seconds
        if x.stop_id in consider_stops:
            pt_bis[x.stop_id].add((x.time_seconds, x.trip))

    kolejnosc_tripow = set()

    for x in pt_bis:
        list1 = sorted(pt_bis[x])
        for i in range(0, len(list1)-1):
            kolejnosc_tripow.add((list1[i][1], list1[i+1][1]))

    (uporzadkowane_tripy, extras2) = dfs_init(kolejnosc_tripow)

    print(uporzadkowane_tripy)

    (ptt4, extras) = dfs_init(ptt3)
    mxx = []
    mxx.append(["", "", ""])
    for ttt in ptt4:
        mxx.append(["", "", ""])
    ptt9 = OperatorStops.objects.filter(stop_id__in=[x for x in ptt4])
    for z in ptt9:
        mxx[len(mxx)-ptt4[z.stop_id]] = [z.stop_id, z.name, 0]
        if z.stop_id in extras:
            mxx[len(mxx)-ptt4[z.stop_id]][2] = 1
    licz = 3
    for zn2 in range(0, len(mxx)):
        for k in pt:
            mxx[zn2].append("")

    for k in pt:
        for uuk in pt[k]:
            if uuk in ptt4:
                mxx[len(mxx)-ptt4[uuk]][len(pt)+2-uporzadkowane_tripy[k]] = get_real_time(pt[k][uuk])
            if uuk=="line_id":
                mxx[0][len(pt)+2-uporzadkowane_tripy[k]] = pt[k][uuk]
        licz = licz+1
    return HttpResponse(json.dumps(mxx, ensure_ascii=False), content_type="application/json; encoding=utf-8")

def index(request):
    template = loader.get_template('pools/index2.html')
    context = {
        'latest_question_list': [],
    }
    return HttpResponse(template.render(context, request))

def index5(request):
    template = loader.get_template('pools/index3.html')
    context = {
        'latest_question_list': [],
    }
    return HttpResponse(template.render(context, request))