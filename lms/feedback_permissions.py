from rest_framework import permissions
from django.shortcuts import get_object_or_404
from lms.models.feedback_models import EventInstanceFeedback
from lms.models.event_models import EventInstance
from lms.models.user_models import UserEnrollment, User
from django.db.models import Q


class FeedbackPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            user = get_object_or_404(User, username=request.data.get("username", None))
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=request.data.get("eventInstanceCode"))
            userCriteria = Q(user=user)
            eventInstanceCriteria = Q(eventInstance=eventInstance)
            return UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists()
        
        return request.method == permissions.SAFE_METHODS
