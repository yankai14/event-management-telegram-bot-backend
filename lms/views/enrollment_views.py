from rest_framework import generics, permissions, mixins
from lms.views.filters.enrollment_filter import EnrollmentFilter
from django_filters.rest_framework import DjangoFilterBackend
from lms.models.user_models import UserEnrollment
from lms.serializers.enrollment_serializers import EnrollmentSerializer


class EnrollmentViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        generics.GenericAPIView):

    queryset = UserEnrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = EnrollmentFilter

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    
        


        