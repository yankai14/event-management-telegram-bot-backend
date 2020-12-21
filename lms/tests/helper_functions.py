from rest_framework.test import APIClient
from lms.models.user_models import User

def login():
    userInfo = {
            "email": "limyk2014@gmail.com", 
            "first_name": "Lim", 
            "last_name": "Yk", 
            "username": 26583923,
            "password": "Tb1932923"
        }
    user = User.objects.create_superuser(**userInfo)
    client = APIClient()

    client.force_authenticate(user=user)

    return client