import django_filters
from django_filters.rest_framework import FilterSet
from lms.models.feedback_models import EventInstanceFeedback

class FeedbackFilter(django_filters.FilterSet):
    
    class Meta:
        model = EventInstanceFeedback
        fields = ['userEnrollment__user__username', 'eventInstance__eventInstanceCode', 'date_created']
        
