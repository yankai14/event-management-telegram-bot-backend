import django_filters
from django_filters.rest_framework import FilterSet
from lms.models.enrollment_models import UserEnrollment


class EnrollmentFilter(FilterSet):
    eventInstance = django_filters.CharFilter(
        field_name="eventInstance__eventInstanceCode", 
        lookup_expr="exact"
    )


    class Meta:
        model = UserEnrollment
        fields =  ["id", "eventInstance"]