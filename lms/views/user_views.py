from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import  mixins
from lms.models.user_models import User
from lms.serializers.user_serializers import UserSerializer

class UserViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_object(self):
        username = self.request.query_params.get("username", None)
        if username is not None:
            self.kwargs["username"] = username
        return super(UserViewSet, self).get_object()

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        if self.request.query_params.get("username", None):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return response
        except IntegrityError:
            return Response({"detail": "Username already exist"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete an event
        """
        return self.destroy(request, *args, **kwargs)


class VerifyToken(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    