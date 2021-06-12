from django.db import models
from . import User, EventInstance


class EventRole(models.IntegerChoices):
    PARTICIPANT = 1
    FACILITATOR = 2
    EVENT_ADMIN = 3
    COORDINATOR = 4
    LEAD = 5

class UserEnrollment(models.Model):
    ''' Store administrative information about participant'''

    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    eventInstance = models.ForeignKey("EventInstance", on_delete=models.CASCADE, null=True)
    paymentPlatform = models.CharField(max_length=200, blank=True, null=True)
    role = models.IntegerField(choices=EventRole.choices, blank=False, null=True)