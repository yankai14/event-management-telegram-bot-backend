from django.db import models
from django.contrib.postgres.fields import ArrayField


class Event(models.Model):

    eventCode = models.CharField(max_length=100, blank=False, null=True, unique=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(default="")


class EventInstance(models.Model):
    ''' An EventInstance is a many to one relation with Event. 
    Eg A module has many tutorial groups. '''
    
    eventInstanceCode = models.CharField(max_length=30, blank=False, null=True)
    startDate = models.DateTimeField(blank=False, null=True)
    endDate = models.DateTimeField(blank=False, null=True)
    location = models.CharField(max_length=250, blank=False, null=True)
    dates = ArrayField(
        models.DateTimeField(blank=False, null=True),
        null=True
    )
    isCompleted = models.BooleanField(default=False)
    event = models.ForeignKey('Event', null=True, on_delete=models.SET_NULL)