import datetime
import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from lms.models.feedback_models import EventFeedback, EventInstanceFeedback
from lms.models.user_models import UserEnrollment
from lms.models.event_models import Event, EventInstance
from lms.tests.helper_functions import login

class EventFeedbackTest(APITestCase):

    def setUp(self):
        user,self.client = login()

        user = {
            "user" : user,
            "paymentId" : "Testing ID",
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }

        testUser = UserEnrollment.objects.create(**user)

        event = {
            "eventCode" : "Test Code",
            "name" : "Test",
            "description" : "Testing purposes",
        }

        testEvent = Event.objects.create(**event)

        EventFeedback.objects.create(userEnrollment=testUser, event=testEvent, eventFeedback="test")

    
        

