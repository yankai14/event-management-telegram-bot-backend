import enum
from django.db import models
from django.contrib.auth.models import AbstractUser


class EventRole(models.IntegerChoices):
    PARTICIPANT = 1
    FACILITATOR = 2
    EVENT_ADMIN = 3
    COORDINATOR = 4
    LEAD = 5
    
class User(AbstractUser):
    pass
    