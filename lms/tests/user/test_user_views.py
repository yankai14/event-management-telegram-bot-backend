from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from lms.models.user_models import User

client = APIClient()

class GetUserViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "username": "12419481",
            "email": "hello@gmail.com",
            "password": "password",
            "first_name": "Hello",
            "last_name": "World"
        }

        User.objects.create(**self.validPayload)

    def test_get_specific_user(self):

        response = client.get(
            reverse("user-view")
        )

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)