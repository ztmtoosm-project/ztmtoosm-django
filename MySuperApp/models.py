# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class OperatorRoutes(models.Model):
    route_id = models.CharField(db_column='route_id', primary_key=True, max_length=20)  # Field name made lowercase.
    direction = models.IntegerField(db_column='direction', primary_key=True)  # Field name made lowercase.
    stop_on_direction_number = models.IntegerField(db_column='stop_on_direction_number', primary_key=True)  # Field name made lowercase.
    stop_id = models.CharField(db_column='stop_id', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'operator_routes'
        unique_together = (('route_id', 'direction', 'stop_on_direction_number'),)


class OperatorStops(models.Model):
    stop_id = models.CharField(db_column='stop_id', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='lon', blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='lat', blank=True, null=True)  # Field name made lowercase.
    coordinates_quality = models.IntegerField(db_column='coordinates_quality', blank=True, null=True)  # Field name made lowercase.
    more_info = models.TextField(db_column='more_info', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'operator_stops'


class OsmRelations(models.Model):
    relation_id = models.BigIntegerField(db_column='relation_id', primary_key=True)  # Field name made lowercase.
    ref_id = models.CharField(db_column='ref_id', primary_key=True, max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'osm_relations'
        unique_together = (('relation_id', 'ref_id'),)


class OsmStops(models.Model):
    normal_stop = models.BigIntegerField(db_column='normal_stop', blank=True, null=True)  # Field name made lowercase.
    stop_position = models.BigIntegerField(db_column='stop_position', blank=True, null=True)  # Field name made lowercase.
    ref_id = models.CharField(db_column='ref_id', primary_key=True, max_length=10)  # Field name made lowercase.
    normal_stop_name = models.CharField(db_column='normal_stop_name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stop_position_name = models.CharField(db_column='stop_position_name', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'osm_stops'


class OsmTree(models.Model):
    relation_id = models.BigIntegerField(db_column='relation_id', primary_key=True)  # Field name made lowercase.
    relation_parent = models.ForeignKey('self', models.DO_NOTHING, db_column='relation_parent', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='name', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='type', max_length=1, blank=True, null=True)  # Field name made lowercase.
    route_id = models.CharField(db_column='route_id', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'osm_tree'


class SpecialModel(models.Model):
    normal_stop = models.IntegerField(db_column='normal_stop', null=True)
    stop_position = models.IntegerField(db_column='stop_position', null=True)
    stop_id_1 = models.CharField(db_column='stop_id', primary_key=True,  max_length=20)
    stop_id_2 = models.CharField(db_column='ref_id', null=True,  max_length=20)
    class Meta:
        managed = False
        db_table = 'good_stops'

class RoutesConnectedWithStopModel(models.Model):
    route_id = models.IntegerField(db_column='route_id')
    direction = models.IntegerField(db_column='direction')
    stop_on_direction_number = models.IntegerField(db_column='stop_on_direction_number', primary_key=True)
    stop_id = models.CharField(db_column='stop_id', max_length=20)
    req_id = models.CharField(db_column='req_id', max_length=20)
    name = models.CharField(db_column='name', max_length=255)
    class Meta:
        unique_together = (("route_id", "direction", "stop_on_direction_number"),)
        managed = False
        db_table = 'ztmtoosm_routes_connected_with_stop'