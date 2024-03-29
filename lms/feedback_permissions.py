from rest_framework import permissions
from django.shortcuts import get_object_or_404
from lms.models.feedback_models import EventInstanceFeedback
from lms.models.event_models import EventInstance
from lms.models.user_models import User
from lms.models.enrollment_models import UserEnrollment
from django.db.models import Q


class FeedbackPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST" or request.method == "PUT":
            user = get_object_or_404(User, username=request.data.get("username"))
            eventInstance = get_object_or_404(EventInstance, eventInstanceCode=request.data.get("eventInstanceCode"))
            userCriteria = Q(user=user)
            eventInstanceCriteria = Q(eventInstance=eventInstance)

            return UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists()

        elif request.method == "DELETE":
            userEnrollment = UserEnrollment.objects.get(user=request.user)
            id = view.kwargs.get('pk')
            userCriteria = Q(userEnrollment=userEnrollment)
            idCriteria = Q(id=id)
            return EventInstanceFeedback.objects.filter(userCriteria & idCriteria).exists()

        return request.method in permissions.SAFE_METHODS
