from django.db import models


class Event(models.Model):

    eventCode = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    description = models.TextField()


class EventInstance(models.Model):
    ''' An EventInstance is a many to one relation with Event. 
    Eg A module has many tutorial groups. '''
    
    eventInstanceCode = models.CharField(max_length=30)
    startDate = models.DateField()
    endDate = models.DateField()
    location = models.CharField(max_length=250)
    dates = models.JSONField()
    isCompleted = models.BooleanField(default=False)

    event = models.ForeignKey('Event', on_delete=models.SET_NULL)