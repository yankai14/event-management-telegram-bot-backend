from django.db import models
from . import User, EventInstance

#Added enrollmentStatus field

class EventRole(models.IntegerChoices):
    PARTICIPANT = 1
    FACILITATOR = 2
    EVENT_ADMIN = 3
    COORDINATOR = 4
    LEAD = 5

class EnrollmentStatus(models.IntegerChoices):
    PENDING = 1
    ENROLLED = 2
    REJECTED = 3
    WITHDRAWN = 4
    AWAITING_PAYMENT = 5

class UserEnrollment(models.Model):
    ''' Store administrative information about participant'''

    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    eventInstance = models.ForeignKey("EventInstance", on_delete=models.CASCADE, null=True)
    paymentPlatform = models.CharField(max_length=200, blank=True, null=True)
    role = models.IntegerField(choices=EventRole.choices, blank=False, null=True)
    enrollmentStatus = models.IntegerField(choices=EnrollmentStatus.choices, default=5)