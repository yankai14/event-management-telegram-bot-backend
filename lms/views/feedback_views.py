from rest_framework import permissions, mixins, generics
from lms.models.feedback_models import EventInstanceFeedback
from lms.serializers.feedback_serializers import EventInstanceFeedbackSerializer
from django_filters.rest_framework import DjangoFilterBackend
from lms.views.filters.event_instance_feedback_filter import FeedbackFilter
from lms.feedback_permissions import FeedbackPermission


class EventInstanceFeedbackViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    
    queryset = EventInstanceFeedback.objects.all()
    serializer_class = EventInstanceFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated,
                          FeedbackPermission]
                          
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter

    def get(self,request,*args,**kwargs):
        if kwargs.get("pk"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
        

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)