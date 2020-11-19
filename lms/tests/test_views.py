import json
import random
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from lms.views import EventView
from lms.models import Event


client = APIClient()


class EventViewTest(APITestCase):

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

    def test_get_event_list(self):

        Event.objects.create(**self.validPayload)

        response = client.get(
            reverse("event-view")
        )
        self.assertEqual(len(response.data["results"]), 1)
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
