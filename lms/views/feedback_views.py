from rest_framework import permissions, mixins, generics
from lms.models.feedback_models import EventInstanceFeedback
from lms.serializers.feedback_serializers import EventInstanceFeedbackSerializer


class EventInstanceFeedbackViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    
    queryset = EventInstanceFeedback.objects.all()
    serializer_class = EventInstanceFeedbackSerializer

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]    

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