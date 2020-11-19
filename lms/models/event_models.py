from django.db import models


class Event(models.Model):

    eventCode = models.CharField(max_length=30, blank=False, null=True, unique=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(default="")


class EventInstance(models.Model):
    ''' An EventInstance is a many to one relation with Event. 
    Eg A module has many tutorial groups. '''
    
    eventInstanceCode = models.CharField(max_length=30, blank=False, null=True)
    startDate = models.DateField(blank=False, null=True)
    endDate = models.DateField(blank=False, null=True)
    location = models.CharField(max_length=250, blank=False, null=True)
    dates = models.JSONField(blank=False, null=True)
    isCompleted = models.BooleanField(default=False)

    event = models.ForeignKey('Event', null=True, on_delete=models.SET_NULL)