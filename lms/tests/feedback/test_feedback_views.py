import datetime
import json
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.generics import get_object_or_404
from lms.models.feedback_models import EventInstanceFeedback
from lms.models.user_models import UserEnrollment
from lms.models.event_models import Event, EventInstance
from lms.tests.helper_functions import login

class GetEventInstanceFeedbackTest(APITestCase):

    def setUp(self):
        self.user,self.client = login()


        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes",
        }

        testEvent = Event.objects.create(**event)

        eventInst ={
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }

        testEnrollment = UserEnrollment.objects.create(**userEnrollment)

        EventInstanceFeedback.objects.create(userEnrollment=testEnrollment, eventInstance=testEventInstance, eventInstanceFeedback="Testing Feedback")

    
    def test_get_event_instance_feedback(self):
        response = self.client.get(
            reverse("event-instance-feedback-view"),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostEventInstanceFeedbackTest(APITestCase):
    
    def setUp(self):
        
        self.user, self.client = login()

        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes",
        }

        testEvent = Event.objects.create(**event)

        eventInst ={
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }

        testEnrollment = UserEnrollment.objects.create(**userEnrollment)
        
        self.validPayload = {
            "username" : self.user.username,
            "eventInstanceCode" : testEnrollment.eventInstance.eventInstanceCode,
            "eventInstanceFeedback" : "testing feedback",
        }

    def test_create_event_instance_feedback(self):
        
        response = self.client.post(
            reverse("event-instance-feedback-view"),
            data=json.dumps(self.validPayload),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_instance_feedback_unauthenticated(self):

        self.client = APIClient()
        response = self.client.post(
            reverse("event-instance-feedback-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class RetrieveEventInstanceFeedbackTest(APITestCase):

    def setUp(self):

        self.user, self.client = login()

        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes"
        }

        testEvent = Event.objects.create(**event)

        eventInst = {
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }            
        #From userEnrollment model, one of field is user which ORM to User model.
        #Hence, from helper_function, user obj is created from User.
        testEnrollment = UserEnrollment.objects.create(**userEnrollment)

        self.eventInstanceFeedback = EventInstanceFeedback.objects.create(userEnrollment=testEnrollment, eventInstance=testEventInstance, eventInstanceFeedback="Testing Feedback")

    def test_retrieve_event_instance_feedback(self):
        
        response = self.client.get(
            reverse('event-instance-feedback-view', kwargs={'pk':self.eventInstanceFeedback.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UpdateEventInstanceFeedbackTest(APITestCase):
    
    def setUp(self):

        self.user, self.client = login()

        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes"
        }

        testEvent = Event.objects.create(**event)

        eventInst = {
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }            
        #From userEnrollment model, one of field is user which ORM to User model.
        #Hence, from helper_function, user obj is created from User.
        testEnrollment = UserEnrollment.objects.create(**userEnrollment)

        self.testEventInstanceFeedback = EventInstanceFeedback.objects.create(userEnrollment=testEnrollment, eventInstance=testEventInstance, eventInstanceFeedback="Testing Feedback")

        self.updatedPayload = {
            "username" : self.user.username,
            "eventInstanceCode" : testEnrollment.eventInstance.eventInstanceCode,
            "eventInstanceFeedback" : "updated testing feedback"
        }
    
    def test_update_event_instance_feedback(self):
        
        response = self.client.put(
            reverse('event-instance-feedback-view', kwargs={"pk":self.testEventInstanceFeedback.id}),
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

class DeleteEventInstanceFeedback(APITestCase):
     
    def setUp(self):
        
        self.user, self.client = login()

        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes"
        }

        testEvent = Event.objects.create(**event)

        eventInst = {
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }            
        #From userEnrollment model, one of field is user which ORM to User model.
        #Hence, from helper_function, user obj is created from User.
        testEnrollment = UserEnrollment.objects.create(**userEnrollment)

        self.eventInstanceFeedback = EventInstanceFeedback.objects.create(userEnrollment=testEnrollment, eventInstance=testEventInstance, eventInstanceFeedback="Testing Feedback")

    def test_delete_event_instance_feedback(self):
        
        response = self.client.delete(reverse('event-instance-feedback-view', kwargs={'pk':self.eventInstanceFeedback.id}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EventInstanceFeedbackFilterTest(APITestCase):

    def setUp(self):

        self.user, self.client = login()

        event = {
            "eventCode" : "T102",
            "name" : "Test",
            "description" : "Testing purposes",
        }

        testEvent = Event.objects.create(**event)

        eventInst ={
            "eventInstanceCode" : "Test102",
            "startDate" : timezone.now(),
            "endDate" : timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0            
        }

        testEventInstance = EventInstance.objects.create(**eventInst)

        userEnrollment = {
            "user" : self.user,
            "paymentId" : "Testing ID",
            "eventInstance" : testEventInstance,
            "paymentPlatform" : "Testing Platform",
            "role" : 1,
        }

        testEnrollment = UserEnrollment.objects.create(**userEnrollment)
        
        testEventInstanceFeedback = EventInstanceFeedback.objects.create(userEnrollment=testEnrollment, eventInstance=testEventInstance, eventInstanceFeedback='Testing Feedback')

    def test_event_instance_feedback_filter_username(self):
        
        response = self.client.get(
            f"{reverse('event-instance-feedback-view')}?userEnrollment__user__username=yankai14&eventInstance__eventInstanceCode=&date_created="
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
    
    def test_event_instance_feedback_filter_event_instance_code(self):

        response = self.client.get(
            f"{reverse('event-instance-feedback-view')}?userEnrollment__user__username=&eventInstance__eventInstanceCode=Test102&date_created="
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

