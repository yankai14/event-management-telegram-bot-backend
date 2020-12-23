import datetime
import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from lms.models.event_models import Event, EventInstance
from lms.tests.helper_functions import login


class PostEnrollmentViewTest(APITestCase):

    def setUp(self):

        event = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        testEvent = Event.objects.create(**event)

        eventInstance = {
            "eventInstanceCode": "Test101",
            "startDate": timezone.now(),
            "endDate": timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent
        }

        EventInstance.objects.create(**eventInstance)

        self.validPayload = {
            "username": 26583923,
            "eventInstanceCode": "Test101",
            "role": 1
        }

        self.client = login()

    def test_create_enrollment(self):

        response = self.client.post(
            reverse("enrollment-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_enrollment_unauthenticated(self):
        
        client = APIClient()
        response = client.post(
            reverse("enrollment-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)