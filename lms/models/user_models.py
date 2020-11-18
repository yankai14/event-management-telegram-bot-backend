from django.db import models
from django.contrib.auth import models as Auth


class Coordinator(models.Model):
    ''' In an training session, these are trainers.'''

    user = models.OneToOneField(Auth.User, on_delete=models.CASCADE)
    # team = models.ForeignKey('Team', on_delete=models.SET_NULL)


class Administrator(models.Model):

    user = models.OneToOneField(Auth.User, on_delete=models.CASCADE)
    pass


class Participant(models.Model):

    user = models.OneToOneField(Auth.User, on_delete=models.CASCADE)
    pass


class Team(models.Model):
    pass


class UserEnrollment(models.Model):
    pass