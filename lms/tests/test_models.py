from rest_framework.test import APITestCase
from lms.models import Event


class EventModelTest(APITestCase):

    def setUp(self):
        Event.objects.create(
            name="event1",
            description="This is my description",
        )

