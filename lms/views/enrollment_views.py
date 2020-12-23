from rest_framework import generics, status, permissions
from rest_framework.response import Response
from lms.serializers.enrollment_serializers import EnrollmentSerializer
from lms.permissions import EventInstancePermission
import json


class EnrollmentViewSet(generics.GenericAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [EventInstancePermission(), permissions.IsAdminUser()]
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

    def post(self, request, *args, **kwargs):
        payload = json.loads(request.body)
        serializer = EnrollmentSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        


        