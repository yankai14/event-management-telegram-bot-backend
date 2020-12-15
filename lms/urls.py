from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from lms import views


urlpatterns = [
    path('event', views.event_views.EventViewSet.as_view(), name='event-view'),
    path('event/event-instance', views.event_views.EventInstanceViewSet.as_view({'get': 'list', 'delete': 'destroy', 'post': 'create'}), name='event-instance-view'),
    path('event/event-instance/<str:eventInstanceCode>/', views.event_views.EventInstanceViewSet.as_view({'get': 'retrieve'}), name='retrieve-event-instance-view'),
    path('auth/user', views.user_views.UserViewSet.as_view(), name='user-view'),
    path('auth/login', obtain_auth_token, name='api_token_auth')
]