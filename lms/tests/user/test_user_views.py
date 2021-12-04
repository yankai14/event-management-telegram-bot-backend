from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from lms.models.user_models import User
from lms.tests.helper_functions import login
import json

class GetUserViewTest(APITestCase):

    def setUp(self):

        self.user, self.client = login()

        validPayload = {
            "username": "12419481",
            "email": "hello@gmail.com",
            "password": "password",
            "first_name": "Hello",
            "last_name": "123"
        }

        User.objects.create(**validPayload)

    def test_get_users(self):

        response = self.client.get(
            reverse("user-view")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_specific_user(self):

        response = self.client.get(
            reverse("user-view")
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][1]['username'], "12419481")

    def test_get_null_user(self):

        response = self.client.get(
            reverse("user-view", kwargs={"username":"nulluser"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
class CreateUserViewTest(APITestCase):

    def setUp(self):
        
        self.user, self.client = login()

        user = {
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "password": "testuser"
        }

        User.objects.create(**user)

        self.duplicatedPayload = {
            "email": "limyk2014@gmail.com", 
            "first_name": "Lim", 
            "last_name": "Yk", 
            "username": "yankai14",
            "password": "Tb1932923"
        }

    def test_create_user(self):

        response = self.client.get(
            reverse("user-view", kwargs={"username":"testuser"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_duplicate_user(self):
        
        response = self.client.post(
            reverse("user-view"),
            data = json.dumps(self.duplicatedPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteUserTest(APITestCase):
    
    def setUp(self):
        self.user, self.client = login()

        user = {
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "password": "testuser"            
        }

        User.objects.create(**user)

    def test_delete_user(self):
        
        response = self.client.delete(
            reverse("user-view", kwargs={"username":"testuser"})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    

class FilterUserTest(APITestCase):

    def setUp(self):
        self.user, self.client = login()

        user = {
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "username": "testuser",
            "password": "testuser"            
        }

        User.objects.create(**user)
    
    def test_user_filter_username(self):
        
        response = self.client.get(
            f"{reverse('user-view')}?username=testuser&first_name=&last_name=&email="
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['username'],'testuser')

    def test_user_filter_first_name(self):
        
        response = self.client.get(
            f"{reverse('user-view')}?username=&first_name=test&last_name=&email="
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['first_name'],'test')
    
    def test_user_filter_last_name(self):
        
        response = self.client.get(
            f"{reverse('user-view')}?username=&first_name=&last_name=user&email="
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['last_name'],'user')    

    def test_user_filter_email(self):
        
        response = self.client.get(
            f"{reverse('user-view')}?username=&first_name=&last_name=&email=testuser@gmail.com"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['email'],'testuser@gmail.com')    