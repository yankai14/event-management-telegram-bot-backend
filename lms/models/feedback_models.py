from django.db import models
from . import Event, EventInstance, UserEnrollment

class EventInstanceFeedback(models.Model):

    userEnrollment = models.ForeignKey('UserEnrollment', null=True,on_delete=models.CASCADE)
    eventInstance = models.ForeignKey('EventInstance', null=True, on_delete=models.CASCADE)
    eventInstanceFeedback = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.eventInstanceFeedback



    
    
    