from rest_framework.test import APITestCase
from lms.models import Event


class EventModelTest(APITestCase):

    def setUp(self):
        Event.objects.create(
            eventCode="T101",
            name="testEvent",
            description="This is my description",
        )
        