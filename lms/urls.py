from django.urls import path
from lms import views


urlpatterns = [
    path('event', views.event_views.EventViewSet.as_view(), name='event-view'),
    path('event/event-instance', views.event_views.EventInstanceViewSet.as_view({'get': 'list', 'delete': 'destroy', 'post': 'create'}), name='event-instance-view'),
    path('event/event-instance/<str:eventInstanceCode>', views.event_views.EventInstanceViewSet.as_view({'get': 'retrieve'}, name='event-instance-view-retrieve')),
    path('auth/user', views.user_views.UserViewSet.as_view(), name='user-view')
]