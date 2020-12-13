from rest_framework import serializers
from lms.models.user_models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }


    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name = validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user