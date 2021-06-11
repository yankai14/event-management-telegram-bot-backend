from django.db import models
from . import User, EventRole, EventInstance


class UserEnrollment(models.Model):
    ''' Store administrative information about participant'''

    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    eventInstance = models.ForeignKey("EventInstance", on_delete=models.CASCADE, null=True)
    paymentPlatform = models.CharField(max_length=200, blank=True, null=True)
    role = models.IntegerField(choices=EventRole.choices, blank=False, null=True)