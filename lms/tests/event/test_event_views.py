import json
import random
import datetime
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from lms.models.event_models import Event, EventInstance


client = APIClient()


class GetEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

    def test_get_specific_event(self):
        
        Event.objects.create(**self.validPayload)
        url = f"{reverse('event-view')}?eventCode=T101"
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_list_pagination(self):

        for n in range(51):
            payload = self.validPayload
            payload["eventCode"] += str(n)
            Event.objects.create(**payload)

        response = client.get(
            reverse("event-view")
        )
        self.assertEqual(len(response.data["results"]), 50)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.invalidPayload = {
            "eventCode": "",
            "name": "invalidTestEvent",
            "description": "This is my description"
        }


    def test_create_valid_event(self):

        response = client.post(
            reverse("event-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        proposed_response = response.data
        del proposed_response['id']

        self.assertDictEqual(self.validPayload, proposed_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event_no_event_code(self):

        response = client.post(
            reverse("event-view"),
            data=json.dumps(self.invalidPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicated_event(self):

        Event.objects.create(**self.validPayload)

        response = client.post(
            reverse("event-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.updatedPayload = {
            "eventCode": "T101",
            "name": "updatedTestEvent",
            "description": "This is my description"
        }

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_update_event(self):

        url = f"{reverse('event-view')}?eventCode=T101"
        response = client.put(
            url,
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteEventViewTest(APITestCase):
    
    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_delete_event(self):

        url = f"{reverse('event-view')}?eventCode=T101"
        response = client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GetEventInstanceViewTest(APITestCase):

    def setUp(self):

        testEvent = Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventInstanceCode": "Test101",
            "startDate": timezone.now(),
            "endDate": timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent
        }
        self.testEventInstance = EventInstance.objects.create(**self.validPayload)

    def test_get_specific_event_instance_by_event_code(self):
        
        url = f"{reverse('event-instance-view')}?eventCode=Test101"
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_isCompleted(self):
        
        url = f"{reverse('event-instance-view')}?isCompleted=False"
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_event_instance_list(self):

        response = client.get(
            reverse("event-instance-view")
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateEventInstanceViewTest(APITestCase):

    def setUp(self):

        Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": False,
        }

    def test_create_valid_event(self):

        url = reverse('event-instance-view')
        response = client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)