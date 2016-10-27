from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.db.models import Q
from django.http import JsonResponse
import json
import re

class waw_settings:
    def get_type_small(line):
        return "bus"
    def get_type_large(line):
        return "Bus"
    def handle_endstop_name(name):
        #rr = re.compile("(?P<lol>([\W\)\(]+\s*)*)\s*\d*")
        #print (re.match(rr, name).group("lol"))
        return name

def get_tracks(lin):
    if good_stops2 is False:
        return None
    directions = OperatorRoutes.objects.filter(route_id=lin).values_list('direction', flat=True).distinct()
    for direction in directions:
        OperatorRoutes.objects.filter(route_id=lin, direction=direction).order_by('stop_on_direction_number')

def get_info(lin):
    tz2 = OsmTree.objects.filter(route_id=lin).values_list('relation_id', flat=True)
    tz2a = OsmTree.objects.filter(route_id=lin, type='m').values_list('relation_id', flat=True)
    tz2b = OsmTree.objects.filter(route_id=lin, type='r').values_list('relation_id', flat=True)
    tz3 = OsmRelations.objects.filter(relation_id__in=tz2).values_list('ref_id', flat=True).distinct()
    tz4 = OperatorRoutes.objects.filter(route_id=lin).values_list('stop_id', flat=True).distinct()
    tz5 = len({entry for entry in tz4} - {entry for entry in tz3})
    tz6 = len({entry for entry in tz3} - {entry for entry in tz4})
    ok = tz5 == 0 and tz6 == 0
    return {'ok' : ok, 'lin' : lin, 'toadd' : tz5, 'todelete' : tz6, 'master' : tz2a, 'nmaster' : tz2b}

def good_stops2(lin, tz3=None):
    if tz3 is None:
        tz3 = SpecialModel.objects.filter(Q(stop_position__isnull=False), ~Q(stop_position=0))
    tz2 = OperatorRoutes.objects.filter(route_id=lin)
    tz4 = [a.stop_id_1 for a in tz3]
    for ob2 in tz2:
            if(ob2.stop_id in tz4):
                pass
            else:
                return False
    return True

def good_stops(lin, tz3=None):
    if good_stops2(lin, tz3) is False:
        return None
    tz = OperatorRoutes.objects.filter(route_id=lin).values_list('direction', flat=True).distinct()
    if len(tz) is 0:
        return None

    ret = []
    for ob1 in tz:
        ret1 = []
        tz2 = OperatorRoutes.objects.filter(route_id=lin, direction=ob1).order_by('stop_on_direction_number')
        for ob2 in tz2:
            try:
                tz3 = OperatorStops.objects.get(stop_id=ob2.stop_id)
            except OperatorStops.DoesNotExist:
                return None
            try:
                tz4 = OsmStops.objects.get(ref_id=ob2.stop_id)
            except OsmStops.DoesNotExist:
                return None
            if tz4.stop_position is None or tz4.stop_position==0:
                return None
            ret1.append({'name_operator' : tz3.name, 'name_osm' : tz4.stop_position_name, 'stop_position' : tz4.stop_position, 'stop' : tz4.normal_stop or tz4.stop_position})
        ret.append(ret1)
    return ret

def master_json(masters, id, childs):
    if len(masters) == 0:
        masters = [-99]
    ret = {"id" : masters[0], "members" : [], "tags" : []}
    for child in childs:
        ret["members"].append({"category" : "R", "role" : '', "id" : child})
    ret['tags'].append({"key" : "ref", "value" : id})
    ret['tags'].append({"key" : "route_master", "value" : waw_settings.get_type_small(id)})
    ret['tags'].append({"key" : "name", "value" : waw_settings.get_type_large(id)+" "+id})
    ret['tags'].append({"key" : "public_transport:version", "values" : "2"})
    ret['tags'].append({"key" : "source", "value" : "Rozkład jazdy ZTM Warszawa, trasa wygenerowana przez bot"})
    ret['tags'].append({"key" : "network", "value" : "ZTM Warszawa"})
    return ret


def view2(request, id):
    arry1 = good_stops(id)
    if arry1 is None:
         return HttpResponse(status=404)

    masters_tmp = OsmTree.objects.filter(route_id=id, type='m').values_list('relation_id', flat=True)
    masters = [a for a in masters_tmp]
    if len(masters) == 0:
        masters = [-99]
    slaves_tmp = OsmTree.objects.filter(route_id=id, type='r').values_list('relation_id', flat=True)
    slaves = [a for a in slaves_tmp]
    slaves_len = len(slaves)
    if slaves_len < len(arry1):
        for i in range(slaves_len, len(arry1)):
            slaves.append(-77+i)
    elif slaves_len > len(arry1):
        pass
    arry2 = []
    i = 0
    for part in arry1:
        arry2_tmp = {"id" : slaves[i], "track" : [], "members" : [], "tags" : [], "track_type" : waw_settings.get_type_small(id)}
        j = 0
        part_end = len(part) - 1
        for part2 in part:
            role_suffix = ""
            if j == 0:
                role_suffix = "_entry_only"
            if j == part_end:
                role_suffix = "_exit_only"
            arry2_tmp['track'].append(part2['stop_position'])
            arry2_tmp['members'].append({"category":"N", "id":part2['stop'] ,"role":("stop"+role_suffix)})
            j = j + 1

        arry2_tmp['tags'].append({"key" : "from", "value" : waw_settings.handle_endstop_name(part[0]['name_osm'])})
        arry2_tmp['tags'].append({"key" : "to", "value" : waw_settings.handle_endstop_name(part[part_end]['name_osm'])})
        arry2_tmp['tags'].append({"key" : "route", "value" : waw_settings.get_type_small(id)})
        arry2_tmp['tags'].append({"key" : "type", "value" : "route"})
        arry2_tmp['tags'].append({"key" : "ref", "value" : id})
        arry2_tmp['tags'].append({"key" : "source", "value" : "Rozkład jazdy ZTM Warszawa, trasa wygenerowana przez bot"})
        arry2_tmp['tags'].append({"key" : "network", "value" : "ZTM Warszawa"})
        arry2_tmp['tags'].append({"key" : "public_transport:version", "value" : "2"})
        name = ""
        name += waw_settings.get_type_large(id)+" "+id+": "
        name += waw_settings.handle_endstop_name(part[0]['name_osm'])
        name += " => "
        name += waw_settings.handle_endstop_name(part[part_end]['name_osm'])
        arry2_tmp['tags'].append({"key" : "name", "value" : name})
        arry2.append(arry2_tmp)
        i = i + 1
    arry2.append(master_json(masters, id, slaves))
    return HttpResponse(json.dumps(arry2, ensure_ascii=False), content_type="application/json; encoding=utf-8")

def index(request):
    tz3 = SpecialModel.objects.filter(Q(stop_position__isnull=False), ~Q(stop_position=0))
    latest_question_list = []
    for val in OperatorRoutes.objects.values_list('route_id', flat=True).distinct():
        latest_question_list.append(get_info(val))

    template = loader.get_template('pools/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))