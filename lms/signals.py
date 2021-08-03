from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query_utils import Q
from lms.models.user_models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from lms.models.event_models import EventInstance
from lms.models.enrollment_models import UserEnrollment, EnrollmentStatus, EventRole
from lms.models.event_models import EventInstanceFolder, EventInstanceFolderPermissions
from lms.serializers.event_serializers import EventInstanceFolderSerializer, EventInstanceFolderPermissionsSerializer


class Signals:

    @staticmethod
    @receiver(post_save, sender=EventInstance)
    def create_folder(sender, instance: EventInstance, created, **kwargs):
        if created:
            data = {
                "folderName": f"Materials: {instance.eventInstanceCode}",
                "eventInstanceCode": instance.eventInstanceCode
            }
            serializer = EventInstanceFolderSerializer(data=data)
            serializer.is_valid()
            serializer.create(serializer.validated_data)


    @staticmethod
    @receiver(post_save, sender=UserEnrollment)
    def create_folder_permission(sender, instance: UserEnrollment, **kwargs):
        eventInstanceFolder = EventInstanceFolder.objects.get(
            eventInstance=instance.eventInstance)
        try:
            permission = EventInstanceFolderPermissions.objects.get(
                folder=eventInstanceFolder, user=instance.user)
            permission.delete()
        except ObjectDoesNotExist:
            pass

        if instance.status == EnrollmentStatus.ENROLLED and instance.role >= EventRole.FACILITATOR:
            data = {
                "folderId": eventInstanceFolder.folderId,
                "folderRole": "writer",
                "username": instance.user.username
            }
            serializer = EventInstanceFolderPermissionsSerializer(data=data)
            serializer.is_valid()
            serializer.create(serializer.validated_data)
        elif instance.status == EnrollmentStatus.ENROLLED and instance.role == EventRole.PARTICIPANT:
            data = {
                "folderId": eventInstanceFolder.folderId,
                "folderRole": "reader",
                "username": instance.user.username
            }
            serializer = EventInstanceFolderPermissionsSerializer(data=data)
            serializer.is_valid()
            serializer.create(serializer.validated_data)

    @staticmethod
    @receiver(post_save, sender=UserEnrollment)
    def update_event_instance_vacancies(sender, instance: UserEnrollment, **kwargs):
        print(instance.eventInstance.vacancy)
        eventInstanceCriteria = Q(eventInstance = instance.eventInstance)
        roleCriteria = Q(role = EventRole.PARTICIPANT)
        statusCriteria = Q(status = EnrollmentStatus.ENROLLED)
        enrollmentCount = UserEnrollment.objects.filter(eventInstanceCriteria & roleCriteria & statusCriteria).count()
        vacancyLeft = instance.eventInstance.vacancy - enrollmentCount
        print(enrollmentCount)
        instance.eventInstance.vacancyLeft = vacancyLeft
        instance.eventInstance.isOpenForSignUps = False if vacancyLeft == 0 else True
        instance.eventInstance.save()
        
