import os
from dotenv import load_dotenv
import stripe
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import status
from stripe.api_resources.checkout import session
from lms.models import User, UserEnrollment


load_dotenv()

stripe.api_key = os.getenv(f"STRIPE_SECRETIVE_KEY")

class StripeCheckoutViewSet(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        eventInstanceCode = request.data.get('eventInstanceCode', None)
        if username and eventInstanceCode:
            return redirect(reverse('enrollment-view', kwargs={'user__username':username, 'eventInstance__eventInstanceCode':eventInstanceCode}))

class StripeCheckoutGatewayViewSet(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAdminUser()]    
    
    def get(self, request, *args, **kwargs):
        username = request.session.get("username")
        eventInstanceCode = request.session.get('eventInstanceCode')
        fee = request.session.get('fee')
        enrollmentStatus = request.session.get('enrollmentStatus')
        if username and eventInstanceCode and fee and enrollmentStatus:
            session = stripe.checkout.Session.create(
                metadata = {
                        "username": username,
                        "eventInstanceCode": eventInstanceCode
                    },
                payment_method_types=['card'],
                line_items=[{
                'price_data': {
                    'currency': 'sgd',
                    'product_data': {
                    'name': eventInstanceCode,
                    },
                    'unit_amount': round(float(fee)*100),
                },
                'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/stripe-success',
                cancel_url='http://127.0.0.1:8000/stripe-failed'
            )
            stripe_url = session.url
            return JsonResponse({"stripe_checkout_url":stripe_url})
        else:
            print("Information not found!")
            return Response(status=status.HTTP_404_NOT_FOUND)
            


class StripeCheckoutWebhook(APIView):

    def post(self, request, *args, **kwargs):
        endpoint_secret = os.getenv(f"STRIPE_WEBHOOK_KEY")
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )

        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session_metadata = event['data']['object']["metadata"]
            username = session_metadata.get("username")
            eventInstanceCode = session_metadata.get("eventInstanceCode")
            user_enrolled = UserEnrollment.objects.filter(user__username__exact=username, eventInstance__eventInstanceCode__exact=eventInstanceCode).values()
            if user_enrolled:
                user_enrolled.update(enrollmentStatus=2)
                

        return Response(status=status.HTTP_200_OK)


def stripe_success_page(request):
    return render(request, "stripe_success_page.html")

def stripe_failed_page(request):
    return render(request, "stripe_failed_page.html")