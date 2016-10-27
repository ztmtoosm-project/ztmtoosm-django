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
    route_id = models.CharField(db_column='ROUTE_ID', primary_key=True, max_length=20)  # Field name made lowercase.
    direction = models.IntegerField(db_column='DIRECTION', primary_key=True)  # Field name made lowercase.
    stop_on_direction_number = models.IntegerField(db_column='STOP_ON_DIRECTION_NUMBER', primary_key=True)  # Field name made lowercase.
    stop_id = models.CharField(db_column='STOP_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPERATOR_ROUTES'
        unique_together = (('route_id', 'direction', 'stop_on_direction_number'),)


class OperatorStops(models.Model):
    stop_id = models.CharField(db_column='STOP_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='LON', blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='LAT', blank=True, null=True)  # Field name made lowercase.
    coordinates_quality = models.IntegerField(db_column='COORDINATES_QUALITY', blank=True, null=True)  # Field name made lowercase.
    more_info = models.TextField(db_column='MORE_INFO', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPERATOR_STOPS'


class OsmRelations(models.Model):
    relation_id = models.BigIntegerField(db_column='RELATION_ID', primary_key=True)  # Field name made lowercase.
    ref_id = models.CharField(db_column='REF_ID', primary_key=True, max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OSM_RELATIONS'
        unique_together = (('relation_id', 'ref_id'),)


class OsmStops(models.Model):
    normal_stop = models.BigIntegerField(db_column='NORMAL_STOP', blank=True, null=True)  # Field name made lowercase.
    stop_position = models.BigIntegerField(db_column='STOP_POSITION', blank=True, null=True)  # Field name made lowercase.
    ref_id = models.CharField(db_column='REF_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    normal_stop_name = models.CharField(db_column='NORMAL_STOP_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stop_position_name = models.CharField(db_column='STOP_POSITION_NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OSM_STOPS'


class OsmTree(models.Model):
    relation_id = models.BigIntegerField(db_column='RELATION_ID', primary_key=True)  # Field name made lowercase.
    relation_parent = models.ForeignKey('self', models.DO_NOTHING, db_column='RELATION_PARENT', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    route_id = models.CharField(db_column='ROUTE_ID', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OSM_TREE'


class SpecialModel(models.Model):
    normal_stop = models.IntegerField(db_column='NORMAL_STOP', null=True)
    stop_position = models.IntegerField(db_column='STOP_POSITION', null=True)
    stop_id_1 = models.CharField(db_column='STOP_ID', primary_key=True,  max_length=20)
    stop_id_2 = models.CharField(db_column='REF_ID', null=True,  max_length=20)
    class Meta:
        managed = False
        db_table = 'GOOD_STOPS'