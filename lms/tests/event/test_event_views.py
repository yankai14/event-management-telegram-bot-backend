import json
import datetime
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from lms.models.event_models import Event, EventInstance
from lms.tests.helper_functions import login


class GetEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.user, self.client = login()


    def test_get_specific_event(self):
        
        Event.objects.create(**self.validPayload)
        url = reverse('event-view', kwargs={"eventCode": "T101"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_list_pagination(self):

        for n in range(51):
            payload = self.validPayload
            payload["eventCode"] += str(n)
            Event.objects.create(**payload)

        response = self.client.get(
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

        self.user, self.client = login()

    def test_create_valid_event(self):

        response = self.client.post(
            reverse("event-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        proposed_response = response.data
        del proposed_response['id']

        self.assertDictEqual(self.validPayload, proposed_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event_no_event_code(self):

        response = self.client.post(
            reverse("event-view"),
            data=json.dumps(self.invalidPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicated_event(self):

        Event.objects.create(**self.validPayload)

        response = self.client.post(
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

        self.user, self.client = login()

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_update_event(self):

        url = reverse('event-view', kwargs={"eventCode": "T101"})
        response = self.client.put(
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

        self.user, self.client = login()

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_delete_event(self):

        url = reverse('event-view', kwargs={"eventCode":"T101"})
        response = self.client.delete(url)

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
        self.user, self.client = login()
        self.testEventInstance = EventInstance.objects.create(**self.validPayload)

    def test_get_specific_event_instance_by_event_instance_code(self):
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Test101"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_invalid_event_instance_code(self):
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Invalid"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_specific_event_instance_by_event_code(self):
        
        url = f"{reverse('event-instance-view')}?event=Test101"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_isCompleted(self):
        
        url = f"{reverse('event-instance-view')}?isCompleted=False"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_invalid_event_code(self):
        
        url = f"{reverse('event-instance-view')}?event=Invalid"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)
    
    def test_get_event_instance_list(self):

        response = self.client.get(
            reverse("event-instance-view")
        )
        self.assertEqual(response.data.get("count"), 1)
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
            "isCompleted": "True",
        }
        self.user, self.client = login()

    def test_create_valid_event_instance(self):

        url = reverse('event-instance-view')
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_instance_invalid_eventCode(self):

        url = reverse('event-instance-view')
        self.validPayload["eventCode"] = "T102"
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_event_instance_existing_eventInstanceCode(self):

        validPayload = self.validPayload.copy()
        del validPayload["eventCode"]
        EventInstance.objects.create(**validPayload)
        url = reverse('event-instance-view')
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteEventInstanceViewTest(APITestCase):

    def setUp(self):

        Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": "True",
        }
        self.user, self.client = login()

        validPayload = self.validPayload.copy()
        del validPayload["eventCode"]

        self.testEventInstance = EventInstance.objects.create(**validPayload)

    def test_delete_valid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Test101"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Invalid"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)