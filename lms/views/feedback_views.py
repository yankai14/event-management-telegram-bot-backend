from rest_framework import permissions, mixins, generics
from lms.models.feedback_models import EventInstanceFeedback
from lms.serializers.feedback_serializers import EventInstanceFeedbackSerializer


class EventInstanceFeedbackViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,
                                   generics.GenericAPIView):
    
    queryset = EventInstanceFeedback.objects.all()
    serializer_class = EventInstanceFeedbackSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        print(request.data)
        return self.create(request,*args,**kwargs)
        

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)