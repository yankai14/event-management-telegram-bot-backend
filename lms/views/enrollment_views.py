from django.db.models import query
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from rest_framework import status
from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from lms.models.user_models import User
from lms.views.filters.enrollment_filter import EnrollmentFilter
from django_filters.rest_framework import DjangoFilterBackend
from lms.models.enrollment_models import UserEnrollment
from lms.serializers.enrollment_serializers import EnrollmentSerializer

class MultipleFieldLookupMixin:

    def get_object(self):
        queryset = self.get_queryset()            
        queryset = self.filter_queryset(queryset)  
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: 
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class EnrollmentViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        MultipleFieldLookupMixin,
                        generics.GenericAPIView):

    queryset = UserEnrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EnrollmentFilter
    lookup_fields = ['user__username', 'eventInstance__eventInstanceCode']

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]
    # Overwrite get_queryset to filter against username url parameter.
    # Check documentation for more info https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
    def get_queryset(self):
        queryset = UserEnrollment.objects.all()
        username = self.request.query_params.get("username")
        eventInstanceCode = self.request.query_params.get("eventInstanceCode")
        if username is not None:
            if eventInstanceCode is not None:
                queryset = queryset.filter(user__username=username, eventInstance__eventInstanceCode=eventInstanceCode)
            queryset = queryset.filter(user__username=username)
        return queryset
    
    def session_retrieve(self, request, *args, **kwargs):
        '''Save information into session'''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if serializer.data["enrollmentStatus"] == 5:
            request.session["username"] = serializer.data["user"]
            request.session["eventInstanceCode"] = serializer.data["eventInstance"]["eventInstanceCode"]
            request.session["fee"] = serializer.data["eventInstance"]["fee"]
            request.session["enrollmentStatus"] = serializer.data["enrollmentStatus"]
            return redirect(reverse("event-payment-gateway"))
        else:
            return Response(data=serializer.data)
            
    def get(self, request, *args, **kwargs):
        username_params = kwargs.get("user__username")
        if username_params:
            if kwargs.get("eventInstance__eventInstanceCode"):
                return self.session_retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    
        


        