from django.urls import path
from lms import views


urlpatterns = [
    path('event/', views.EventView.as_view(), name='event-view'),
]