from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.models.event_models import EventInstance


class EventRole(models.Model):

    PARTICIPANT = 1
    FACILITATOR = 2
    EVENT_ADMIN = 3
    COORDINATOR = 4
    LEAD = 5

    ROLE_CHOICES = (
        (PARTICIPANT, 'participant'),
        (FACILITATOR, 'facilitator'),
        (EVENT_ADMIN, 'event_admin'),
        (COORDINATOR, 'coordinator'),
        (LEAD, 'lead')
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)
    eventInstance = models.ForeignKey("EventInstance", on_delete=models.CASCADE, null=True)

    def __str__(self):
      return self.get_id_display()


class UserEnrollment(models.Model):
    ''' Store administrative information about participant'''

    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    eventInstance = models.ForeignKey("EventInstance", on_delete=models.CASCADE, null=True)
    paymentId = models.CharField(max_length=200, blank=True, null=True)
    paymentPlatform = models.CharField(max_length=200, blank=True, null=True)


class User(AbstractUser):

    roles = models.ManyToManyField(EventRole)