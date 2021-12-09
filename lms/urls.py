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
    path("enrollment/<int:pk>", views.enrollment_views.EnrollmentViewSet.as_view(), name="enrollment-view"),
    path("enrollment/<str:user__username>/<str:eventInstance__eventInstanceCode>", views.enrollment_views.EnrollmentViewSet.as_view(), name="enrollment-view"),

    path('event-instance-feedback/', views.feedback_views.EventInstanceFeedbackViewSet.as_view(), name="event-instance-feedback-view"),
    path('event-instance-feedback/<int:pk>', views.feedback_views.EventInstanceFeedbackViewSet.as_view(), name="event-instance-feedback-view"),

    path('event-payment/', views.stripe_checkout_views.StripeCheckoutViewSet.as_view(), name="user-payment"),
    path('event-payment-gateway', views.stripe_checkout_views.StripeCheckoutGatewayViewSet.as_view(), name="event-payment-gateway"),
    path('event-payment/webhook', views.stripe_checkout_views.StripeCheckoutWebhook.as_view(), name="event-payment-webhook"),
    path('stripe-success', views.stripe_success_page, name="stripe-success-page"),
    path('stripe-failed', views.stripe_failed_page, name='stripe-failed-page'),

    path("auth/user", views.user_views.UserViewSet.as_view(), name="user-view"),
    path("auth/user/<str:username>", views.user_views.UserViewSet.as_view(), name="user-view"),
    path("auth/login", obtain_auth_token, name="api_token_auth")
]