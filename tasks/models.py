from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import constants as co


def ValidateGeoPt(value):
  try:
    lat, lon = value.split(',')
    float(lat), float(lon)
  except ValueError:
    raise ValidationError('Geo Pointer should contains lat and lon decimals.')


class Task(models.Model):
  title = models.CharField(max_length=co.TITLE_MAX_LEN)
  overview = models.TextField()
  owner = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name='owner')
  assignee = models.ForeignKey(User, null=True, blank=True,
                               related_name='assignee')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  expired = models.DateTimeField(null=True, blank=True)
  completed = models.DateTimeField(null=True, blank=True)
  end_point = models.CharField(max_length=co.MAX_STRING_LEN)
  geo_location = models.CharField(max_length=co.MAX_STRING_LEN,
                                  validators=[ValidateGeoPt], null=True)
  price = models.DecimalField(null=True, decimal_places=co.DECIMAL_PLACES,
                              max_digits=co.DECIMAL_DIGITS)
  status = models.SmallIntegerField(choices=co.TASK_STATUSES,
                                    default=co.NOT_ASSIGNED)

  class Meta:
    db_table = 'tasks'


class TasksTree(models.Model):
  itype = models.SmallIntegerField(choices=co.ITEM_TYPES,
                                   default=co.TYPE_CATEGORY)
  pid = models.ForeignKey('self', blank=True, null=True)
  name = models.CharField(max_length=co.MAX_STRING_LEN)
  task_id = models.ForeignKey(Task, on_delete=models.PROTECT)

  class Meta:
    db_table = 'taskstree'
