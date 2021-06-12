import datetime
import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from lms.models.enrollment_models import UserEnrollment
from lms.models.event_models import Event, EventInstance
from lms.tests.helper_functions import login


class GetEnrollmentViewTest(APITestCase):

    def setUp(self):
        
        user, self.client = login()

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

        testEventInstance = EventInstance.objects.create(**eventInstance)

        UserEnrollment.objects.create(user=user, eventInstance=testEventInstance, role=1)

    def test_get_user_enrollment(self):

        response = self.client.get(
            reverse("enrollment-view"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostEnrollmentViewTest(APITestCase):

    def setUp(self):

        self.user, self.client = login()

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

        self.eventInstance = EventInstance.objects.create(**eventInstance)

        self.validPayload = {
            "username": self.user.username,
            "eventInstanceCode": "Test101",
            "role": 1
        }


    def test_create_enrollment(self):

        response = self.client.post(
            reverse("enrollment-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_enrollment(self):

        UserEnrollment.objects.create(user=self.user, eventInstance=self.eventInstance, role=1)
        response = self.client.post(
            reverse("enrollment-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        

    def test_create_enrollment_unauthenticated(self):
        
        client = APIClient()
        response = client.post(
            reverse("enrollment-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)