import django_filters
from django_filters.rest_framework import FilterSet
from lms.models.user_models import User

class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']