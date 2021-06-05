from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from lms import views


urlpatterns = [
    path("event", views.event_views.EventViewSet.as_view(), name="event-view"),
    path("event/<str:eventCode>", views.event_views.EventViewSet.as_view(), name="event-view"),

    path("event-instance", views.event_views.EventInstanceViewSet.as_view(), name="event-instance-view"),
    path("event-instance/<str:eventInstanceCode>", views.event_views.EventInstanceViewSet.as_view(), name="event-instance-view"),

    path("event-instance-folder", views.event_views.EventInstanceFolderViewSet.as_view(), name="event-instance-folder-view"),
    path("event-instance-folder/<str:folderId>", views.event_views.EventInstanceFolderViewSet.as_view(), name="event-instance-folder-view"),

    path("event-instance-folder-permissions", views.event_views.EventInstanceFolderPermissionsViewSet.as_view(), name="event-instance-folder-permissions-view"),
    path("event-instance-folder-permissions/<str:permissionId>", views.event_views.EventInstanceFolderPermissionsViewSet.as_view(), name="event-instance-folder-permissions-view"),

    path("enrollment", views.enrollment_views.EnrollmentViewSet.as_view(), name="enrollment-view"),

    path('event-instance-feedback/', views.feedback_views.EventInstanceFeedbackViewSet.as_view(), name="event-instance-feedback-view"),
    path('event-instance-feedback/<int:pk>', views.feedback_views.EventInstanceFeedbackViewSet.as_view(), name="event-instance-feedback-view"),

    path("auth/user", views.user_views.UserViewSet.as_view(), name="user-view"),
    path("auth/user/<str:username>", views.user_views.UserViewSet.as_view(), name="user-view"),
    path("auth/login", obtain_auth_token, name="api_token_auth")
]