from django.urls import path
from lms import views


urlpatterns = [
    path('event', views.event_views.EventViewSet.as_view(), name='event-view'),
    path('event/event-instance', views.event_views.EventInstanceViewSet.as_view(), name='event-instance-view'),
]