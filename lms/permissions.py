from rest_framework import permissions
from lms.models.user_models import UserEnrollment, EventRole
from django.db.models import Q


class EventInstancePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        return UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).exists()


class ParticipantPermission(EventInstancePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        enrollment = UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).first()
        
        return enrollment.get("role", None) == EventRole.PARTICIPANT


class FacilitatorPermission(EventInstancePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        enrollment = UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).first()
        
        return enrollment.get("role", None) == EventRole.FACILITATOR


class EventAdminPermission(EventInstancePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        enrollment = UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).first()
        
        return enrollment.get("role", None) == EventRole.EVENT_ADMIN


class CoordinatorPermission(EventInstancePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        enrollment = UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).first()
        
        return enrollment.get("role", None) == EventRole.COORDINATOR


class LeadPermission(EventInstancePermission):

    def has_permission(self, request, view):
        eventInstanceCode = request.query_params.get("eventInstanceCode", None)
        username = request.user.username

        userCriteria = Q(user__username=username)
        eventInstanceCriteria = Q(eventInstance__eventInstanceCode=eventInstanceCode)
        enrollment = UserEnrollment.objects.filter(userCriteria & eventInstanceCriteria).first()
        
        return enrollment.get("role", None) == EventRole.LEAD