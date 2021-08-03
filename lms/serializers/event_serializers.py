from django.db.models import Q
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from lms.models.event_models import Event, EventInstance, EventInstanceFolder, EventInstanceFolderPermissions
from backend.exception_classes import ModelObjectAlreadyExist
from lms.serializers.user_serializers import UserSerializer
from lms.utils.drive_service import GDriveService
from lms.models.user_models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventInstanceSerializer(serializers.ModelSerializer):

    event = serializers.StringRelatedField()
    eventCode = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = EventInstance
        fields = "__all__"

    def create(self, validated_data: dict):
        if self.is_valid():
            event = get_object_or_404(
                Event, eventCode=validated_data.get("eventCode"))
            if EventInstance.objects.filter(eventInstanceCode=validated_data["eventInstanceCode"]).exists():
                raise ModelObjectAlreadyExist(f"EventInstance already exist")
            else:
                eventInstance = EventInstance.objects.create(
                    eventInstanceCode=validated_data.get("eventInstanceCode"),
                    startDate=validated_data.get("startDate"),
                    endDate=validated_data.get("endDate"),
                    location=validated_data.get("location"),
                    dates=validated_data.get("dates"),
                    fee=validated_data.get("fee", 0),
                    isCompleted=validated_data.get("isCompleted"),
                    event=event
                )
        else:
            raise ValidationError(self.errors)
        return eventInstance


class EventInstanceFolderPermissionsSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    folder = serializers.StringRelatedField()

    class Meta:
        model = EventInstanceFolderPermissions
        fields = "__all__"


class EventInstanceFolderSerializer(serializers.ModelSerializer):

    eventInstance = serializers.StringRelatedField()
    permissions = EventInstanceFolderPermissionsSerializer(
        read_only=True, many=True)
    eventInstanceCode = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = EventInstanceFolder
        fields = "__all__"
        read_only_fields = ["folderId"]

    def create(self, validated_data: dict):
        if self.is_valid():
            eventInstanceCode = validated_data.get("eventInstanceCode")
            eventInstance = get_object_or_404(
                EventInstance, eventInstanceCode=eventInstanceCode)
            folderName = validated_data.get("folderName")

            if not EventInstanceFolder.objects.filter(eventInstance=eventInstance).exists():
                folderId = GDriveService.create_folder(folderName)
                eventInstanceFolder = EventInstanceFolder.objects.create(
                    folderId=folderId,
                    folderName=validated_data.get("folderName"),
                    eventInstance=eventInstance
                )
            else:
                raise ModelObjectAlreadyExist(f"Folder with event instance ${eventInstance} already exist")
        else:
            raise ValidationError(self.errors)

        return eventInstanceFolder


class EventInstanceFolderPermissionsSerializer(serializers.ModelSerializer):

    folder = EventInstanceFolderSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    folderId = serializers.CharField(max_length=200, write_only=True)
    username = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = EventInstanceFolderPermissions
        fields = "__all__"
        read_only_fields = ["permissionId"]

    def create(self, validated_data: dict):
        if self.is_valid():
            folderId = validated_data.get("folderId")
            folderRole = validated_data.get("folderRole")
            username = validated_data.get("username")

            folder = get_object_or_404(EventInstanceFolder, folderId=folderId)
            user = get_object_or_404(User, username=username)

            userCriteria = Q(user=user)
            folderCriteria = Q(folder__folderId=folderId)

            if not EventInstanceFolderPermissions.objects.filter(userCriteria & folderCriteria):
                permissionId = GDriveService.give_permission(
                    fileId=folderId, role=folderRole, granteeEmail=user.email)
                eventInstanceFolderPermission, _ = EventInstanceFolderPermissions.objects.update_or_create(
                    permissionId=permissionId,
                    user=user,
                    folderRole=folderRole
                )
                eventInstanceFolderPermission.folder.add(folder)
            else:
                raise ModelObjectAlreadyExist

        else:
            raise ValidationError(self.errors)

        return eventInstanceFolderPermission
