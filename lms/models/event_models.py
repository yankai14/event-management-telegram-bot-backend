from django.db import models
from django.contrib.postgres.fields import ArrayField


class Event(models.Model):

    eventCode = models.CharField(max_length=100, blank=False, null=True, unique=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(default="")

    def __str__(self):
        return self.eventCode


class EventInstance(models.Model):
    ''' An EventInstance is a many to one relation with Event. 
    Eg A module has many tutorial groups. '''
    
    eventInstanceCode = models.CharField(max_length=100, blank=False, null=True, unique=True)
    startDate = models.DateTimeField(blank=False, null=True)
    endDate = models.DateTimeField(blank=False, null=True)
    location = models.CharField(max_length=250, blank=False, null=True)
    dates = ArrayField(
        models.DateTimeField(blank=False, null=True),
        null=True
    )
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isCompleted = models.BooleanField(default=False)
    event = models.ForeignKey('Event', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.eventInstanceCode