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

class LineDirections(models.Model):
    line = models.CharField(db_column='line', max_length=20)
    trip = models.IntegerField(db_column='trip')
    id2 = models.IntegerField(db_column='id2', primary_key=True)
    name = models.CharField(db_column='name', max_length=255)
    class Meta:
        #unique_together = (("route_id", "direction", "stop_on_direction_number"),)
        managed = False
        db_table = 'line_directions'

class ScheduleTmp(models.Model):
    line = models.CharField(db_column='line', max_length=20)
    trip = models.IntegerField(db_column='trip', primary_key=True)
    next_stop_trip = models.IntegerField(db_column='next_stop_trip', primary_key=True)
    time_seconds = models.IntegerField(db_column='time_seconds')
    day_type = models.CharField(db_column='day_type', max_length=20)
    stop_id = models.CharField(db_column='stop_id', max_length=20)
    direction = models.CharField(db_column='direction', max_length=20)
    class Meta:
        managed = False
        db_table = 'schedule'
        unique_together = (('trip', 'next_stop_trip'),)
