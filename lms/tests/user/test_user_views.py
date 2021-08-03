# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.urls import reverse
# from lms.models.user_models import User
# from lms.tests.helper_functions import login

# class GetUserViewTest(APITestCase):

#     def setUp(self):

#         self.validPayload = {
#             "username": "12419481",
#             "email": "hello@gmail.com",
#             "password": "password",
#             "first_name": "Hello",
#             "last_name": "World"
#         }

#         User.objects.create(**self.validPayload)
#         self.user, self.client = login()

#     def test_get_specific_user(self):

#         response = self.client.get(
#             reverse("user-view")
#         )

#         self.assertEqual(len(response.data["results"]), 2)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)