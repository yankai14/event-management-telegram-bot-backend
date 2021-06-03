import json
import datetime
from typing import OrderedDict
from unittest.mock import MagicMock
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from lms.models.event_models import Event, EventInstance, EventInstanceFolder, EventInstanceFolderPermissions
from lms.models.user_models import User
from lms.tests.helper_functions import login
from lms.utils.drive_service import GDriveService


class GetEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.user, self.client = login()


    def test_get_specific_event(self):
        
        Event.objects.create(**self.validPayload)
        url = reverse('event-view', kwargs={"eventCode": "T101"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_list_pagination(self):

        for n in range(51):
            payload = self.validPayload
            payload["eventCode"] += str(n)
            Event.objects.create(**payload)

        response = self.client.get(
            reverse("event-view")
        )
        self.assertEqual(len(response.data["results"]), 50)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.invalidPayload = {
            "eventCode": "",
            "name": "invalidTestEvent",
            "description": "This is my description"
        }

        self.user, self.client = login()

    def test_create_valid_event(self):

        response = self.client.post(
            reverse("event-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        proposed_response = response.data
        del proposed_response['id']

        self.assertDictEqual(self.validPayload, proposed_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_event_no_event_code(self):

        response = self.client.post(
            reverse("event-view"),
            data=json.dumps(self.invalidPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicated_event(self):

        Event.objects.create(**self.validPayload)

        response = self.client.post(
            reverse("event-view"),
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateEventViewTest(APITestCase):

    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.updatedPayload = {
            "eventCode": "T101",
            "name": "updatedTestEvent",
            "description": "This is my description"
        }

        self.user, self.client = login()

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_update_event(self):

        url = reverse('event-view', kwargs={"eventCode": "T101"})
        response = self.client.put(
            url,
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )
        proposedResponse = response.data
        del proposedResponse['id']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(self.updatedPayload, proposedResponse)

    def test_update_invalid_event(self):

        url = reverse('event-view', kwargs={"eventCode": "T102"})
        response = self.client.put(
            url,
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteEventViewTest(APITestCase):
    
    def setUp(self):

        self.validPayload = {
            "eventCode": "T101",
            "name": "testEvent1",
            "description": "This is my description"
        }

        self.user, self.client = login()

        self.testEvent = Event.objects.create(**self.validPayload)

    def test_delete_event(self):
        url = reverse('event-view', kwargs={"eventCode":"T101"})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event(self):
        url = reverse('event-view', kwargs={"eventCode":"T102"})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class GetEventInstanceViewTest(APITestCase):

    def setUp(self):

        testEvent = Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventInstanceCode": "Test101",
            "startDate": timezone.now(),
            "endDate": timezone.now() + datetime.timedelta(days=10),
            "location": "somewhere",
            "dates": [timezone.now() + datetime.timedelta(days=10+n) for n in range(5)],
            "isCompleted": False,
            "event": testEvent,
            "fee": 0
        }
        self.user, self.client = login()
        self.testEventInstance = EventInstance.objects.create(**self.validPayload)

    def test_get_specific_event_instance_by_event_instance_code(self):
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Test101"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_invalid_event_instance_code(self):
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Invalid"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_specific_event_instance_by_event_code(self):
        
        url = f"{reverse('event-instance-view')}?event=Test101"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_isCompleted(self):
        
        url = f"{reverse('event-instance-view')}?isCompleted=False"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_specific_event_instance_by_invalid_event_code(self):
        
        url = f"{reverse('event-instance-view')}?event=Invalid"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)
    
    def test_get_event_instance_list(self):

        response = self.client.get(
            reverse("event-instance-view")
        )
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateEventInstanceViewTest(APITestCase):

    def setUp(self):

        Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": "True",
            "fee": 0
        }
        self.user, self.client = login()

    def test_create_valid_event_instance(self):

        url = reverse('event-instance-view')
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_instance_invalid_eventCode(self):

        url = reverse('event-instance-view')
        self.validPayload["eventCode"] = "T102"
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_event_instance_existing_eventInstanceCode(self):

        validPayload = self.validPayload.copy()
        del validPayload["eventCode"]
        EventInstance.objects.create(**validPayload)
        url = reverse('event-instance-view')
        response = self.client.post(
            url,
            data=json.dumps(self.validPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteEventInstanceViewTest(APITestCase):

    def setUp(self):

        Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": "True",
            "fee": 0
        }

        self.user, self.client = login()

        validPayload = self.validPayload.copy()
        del validPayload["eventCode"]

        self.testEventInstance = EventInstance.objects.create(**validPayload)

    def test_update_valid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Test101"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Invalid"})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateEventInstanceViewTest(APITestCase):

    def setUp(self):

        Event.objects.create(eventCode="T101", name="testEvent1", description="This is my description")
        self.validPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": "True",
            "fee": 0,
        }
        self.updatedPayload = {
            "eventCode": "T101",
            "eventInstanceCode": "Test101",
            "startDate": str(timezone.now()),
            "endDate": str(timezone.now() + datetime.timedelta(days=10)),
            "location": "somewhere",
            "dates": [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            "isCompleted": "False",
            "fee": 0
        }
        self.user, self.client = login()

        validPayload = self.validPayload.copy()
        del validPayload["eventCode"]

        self.testEventInstance = EventInstance.objects.create(**validPayload)

    def test_update_valid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Test101"})
        response = self.client.put(
            url,
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )
        proposedResponse = response.data
        del proposedResponse['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(proposedResponse["isCompleted"]), self.updatedPayload["isCompleted"])


    def test_update_invalid_event_instance(self):
        
        url = reverse('event-instance-view', kwargs={"eventInstanceCode":"Invalid"})
        response = self.client.put(
            url,
            data=json.dumps(self.updatedPayload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class GetEventInstanceFolderViewTest(APITestCase):

    def setUp(self):
        event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )
        EventInstanceFolder.objects.create(
            folderId = "someTestId",
            folderName = "someFolderName",
            eventInstance = eventInstance
        )

        eventInstance1 = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode1",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )
        EventInstanceFolder.objects.create(
            folderId = "someTestId1",
            folderName = "someFolderName1",
            eventInstance = eventInstance1
        )

        self.expectedOutput = {
            "folderId": "someTestId",
            "folderName": "someFolderName",
            "eventInstance": "someEventInstanceCode"
        }

        #TODO: Create permissions and put into EventInstanceFolder to see if can see

    def test_get_list_of_event_instance_folders(self):

        url = reverse('event-instance-folder-view')
        response = self.client.get(url)
        proposedOutput = response.data["results"][0]
        del proposedOutput['id']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertDictEqual(proposedOutput, self.expectedOutput)

    def test_filter_list_of_event_instance_from_event_instance(self):

        url = f"{reverse('event-instance-folder-view')}?eventInstance=someEventInstanceCode"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class PostEventInstanceFolderViewTest(APITestCase):

    def setUp(self):
        self.event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        self.eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = self.event
        )

        EventInstanceFolder.objects.create(
            folderId = "someFolderId",
            folderName = "someFolderName",
            eventInstance = self.eventInstance
        )

    def test_create_valid_folder(self):

        GDriveService.create_folder = MagicMock(return_value="testId")
        url = reverse('event-instance-folder-view')
        validPayload = {
            "folderName": "testName",
            "eventInstanceCode": "someEventInstanceCode"
        }
        response = self.client.post(
            url,
            data=json.dumps(validPayload),
            content_type="application/json"
        )
        proposedOutput = response.data
        del proposedOutput['id']

        correctData = {
            "eventInstance": "someEventInstanceCode",
            "folderId": "testId",
            "folderName": "testName"
        }

        GDriveService.create_folder.assert_called_once()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(proposedOutput, correctData)

    def test_will_not_create_duplicate_folder_and_return_bad_request(self):
        
        GDriveService.create_folder = MagicMock(return_value="someFolderId")
        validPayload = {
            "folderName": "someFolderName",
            "eventInstanceCode": "someEventInstanceCode"
        }

        url = reverse('event-instance-folder-view')
        response = self.client.post(
            url,
            data=json.dumps(validPayload),
            content_type="application/json"
        )

        GDriveService.create_folder.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteEventInstanceFolderViewTest(APITestCase):

    def setUp(self):
        event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )
        EventInstanceFolder.objects.create(
            folderId = "someTestId",
            folderName = "someFolderName",
            eventInstance = eventInstance
        )

    def test_delete_folder(self):
        GDriveService.delete_file_or_folder = MagicMock()
        url = reverse('event-instance-folder-view', kwargs={'folderId': 'someTestId'})
        response = self.client.delete(url)
        folderExist = EventInstanceFolder.objects.filter(folderId = 'someTestId').exists()
        GDriveService.delete_file_or_folder.assert_called_once_with('someTestId')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(folderExist, False)

    def test_delete_non_existant_folder(self):
        GDriveService.delete_file_or_folder = MagicMock()
        url = reverse('event-instance-folder-view', kwargs={'folderId': 'someIncorrectTestId'})
        response = self.client.delete(url)
        folderExist = EventInstanceFolder.objects.filter(folderId = 'someTestId').exists()
        GDriveService.delete_file_or_folder.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(folderExist, True)


class GetEventFolderPermissionsTest(APITestCase):
    def setUp(self):
        self.user, self.client = login()

        event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )

        folder = EventInstanceFolder.objects.create(
            folderId = "someTestId",
            folderName = "someFolderName",
            eventInstance = eventInstance
        )

        EventInstanceFolderPermissions.objects.create(
            permissionId = 'testId',
            user = self.user,
            folder = folder,
            folderRole = "reader"
        )

        user2 = User.objects.create(
            username = "someUsername",
            email = "someEmail@gmail.com",
            password = "somePassword",
            first_name = "someFirstName",
            last_name = "someLastName"
        )

        EventInstanceFolderPermissions.objects.create(
            permissionId = 'testId2',
            user = user2,
            folder = folder,
            folderRole = "reader"
        )

    def test_get_list_of_permissions(self):
        correctData = {
            "folder": OrderedDict({
                "eventInstance": "someEventInstanceCode",
                "folderId": "someTestId",
                "folderName": "someFolderName"
            }),
            "user": OrderedDict({
                "username": "yankai14",
                "email": "limyk2014@gmail.com",
                "first_name": "Lim",
                "last_name": "Yk"
            }),
            "permissionId": "testId",
            "folderRole": "reader",
        }

        url = reverse('event-instance-folder-permissions-view')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 2)

        proposedOutput = dict(response.data.get("results")[0])
        del proposedOutput['id']
        del proposedOutput['folder']['id']

        self.assertEqual(proposedOutput, correctData)


    def test_get_filtered_list_of_permissions(self):
        correctData = {
            "folder": OrderedDict({
                "eventInstance": "someEventInstanceCode",
                "folderId": "someTestId",
                "folderName": "someFolderName"
            }),
            "user": OrderedDict({
                "username": "yankai14",
                "email": "limyk2014@gmail.com",
                "first_name": "Lim",
                "last_name": "Yk"
            }),
            "permissionId": "testId",
            "folderRole": "reader",
        }

        url = f"{reverse('event-instance-folder-permissions-view')}?user=yankai14&folder=someTestId"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)

        proposedOutput = dict(response.data.get("results")[0])
        del proposedOutput['id']
        del proposedOutput['folder']['id']

        self.assertEqual(proposedOutput, correctData)


class CreateEventFolderPermissionsTest(APITestCase):

    def setUp(self):
        self.user, self.client = login()

        event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )

        EventInstanceFolder.objects.create(
            folderId = "someTestId",
            folderName = "someFolderName",
            eventInstance = eventInstance
        )

    def test_create_permission(self):

        GDriveService.give_permission = MagicMock(return_value="testId")
        validPayload = {
            "folderId": "someTestId",
            "folderRole": "reader",
            "username": self.user.username
        }

        url = reverse('event-instance-folder-permissions-view')

        correctData = {
            "folder": OrderedDict({
                "eventInstance": "someEventInstanceCode",
                "folderId": "someTestId",
                "folderName": "someFolderName"
            }),
            "user": OrderedDict({
                "username": "yankai14",
                "email": "limyk2014@gmail.com",
                "first_name": "Lim",
                "last_name": "Yk"
            }),
            "permissionId": "testId",
            "folderRole": "reader",
        }

        response = self.client.post(
            url, 
            data=json.dumps(validPayload), 
            content_type="application/json"
        )

        proposedOutput = response.data
        del proposedOutput['id']
        del proposedOutput['folder']['id']

        GDriveService.give_permission.assert_called_once_with(fileId='someTestId', role='reader', granteeEmail='limyk2014@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(proposedOutput, correctData)
    
    def test_create_duplicate_permission(self):

        GDriveService.give_permission = MagicMock(return_value="testId")
        validPayload = {
            "folderId": "someTestId",
            "folderRole": "reader",
            "username": self.user.username
        }
        url = reverse('event-instance-folder-permissions-view')
        response = self.client.post(
            url, 
            data=json.dumps(validPayload), 
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        validPayloadDuplicate = {
            "folderId": "someTestId",
            "folderRole": "reader",
            "username": self.user.username
        }

        response = self.client.post(
            url, 
            data=json.dumps(validPayloadDuplicate), 
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class DeleteEventFolderPermissionsTest(APITestCase):

    def setUp(self):
        self.user, self.client = login()

        event = Event.objects.create(
            eventCode = "someEventCode",
            name = "someName",
            description = "someDescription"
        )

        eventInstance = EventInstance.objects.create(
            eventInstanceCode = "someEventInstanceCode",
            startDate = str(timezone.now()), 
            endDate = str(timezone.now() + datetime.timedelta(days=10)),
            location = "somewhere",
            dates = [str(timezone.now() + datetime.timedelta(days=10+n)) for n in range(5)],
            fee = 0,
            isCompleted = False,
            event = event
        )

        folder = EventInstanceFolder.objects.create(
            folderId = "someTestId",
            folderName = "someFolderName",
            eventInstance = eventInstance
        )

        EventInstanceFolderPermissions.objects.create(
            permissionId = 'testId',
            user = self.user,
            folder = folder,
            folderRole = "reader"
        )

    def test_delete_permission(self):
        GDriveService.delete_permission = MagicMock()
        url = reverse('event-instance-folder-permissions-view', kwargs={'permissionId': 'testId'})
        response = self.client.delete(url)
        permissionExist = EventInstanceFolderPermissions.objects.filter(permissionId = 'testId').exists()
        GDriveService.delete_permission.assert_called_once_with('testId')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(permissionExist, False)

    def test_delete_non_existent_permission(self):
        GDriveService.delete_permission = MagicMock()
        url = reverse('event-instance-folder-permissions-view', kwargs={'permissionId': 'wrongId'})
        response = self.client.delete(url)
        permissionExist = EventInstanceFolderPermissions.objects.filter(permissionId = 'testId').exists()
        GDriveService.delete_permission.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(permissionExist, True)