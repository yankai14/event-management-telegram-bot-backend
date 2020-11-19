import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from lms.views import EventView


client = APIClient()


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

    def test_valid_create_event(self):
        response = client.post(
            reverse("create-event"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(json.loads(response.data), self.validPayload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)