from google.oauth2 import service_account
from googleapiclient.discovery import build, MediaFileUpload
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/sqlservice.admin"]
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_OAUTH")

# Authentication
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Make service calls
service = build("drive", "v3", credentials=credentials)


class GDriveService:

    @staticmethod
    def upload_file(filePath: str, fileName: str, folderId: str, mimetypes: str):

        file_metadata = {
            "name": fileName,
            "parents": [folderId]
        }
        media = MediaFileUpload(filePath, mimetype=mimetypes, resumable=True)
        file: dict = service.files().create(body=file_metadata,media_body=media, fields="id").execute()
        fileId = file.get("id")
        return fileId

    @staticmethod
    def delete_file_or_folder(fileId: str):
        service.files().delete(fileId="15M5I0IugIM9t6lx-dpA9OpyeZz3aD9eM").execute()

    @staticmethod
    def create_folder(folderName: str):
        folder_metadata = {
            "name": "Invoices",
            "mimeType": "application/vnd.google-apps.folder"
        }
        folder: dict = service.files().create(body=folder_metadata, fields="id").execute()
        folderId = folder.get("id")
        return folderId

    @staticmethod
    def give_permission(fileId: str, role: str, granteeEmail: str):
        permissions = {
            "type": "user",
            "role": role,
            "emailAddress": granteeEmail
        }

        permission: dict = service.permissions().create(fileId=fileId, body=permissions).execute()
        permissionId = permission.get('id')
        return permissionId

    @staticmethod
    def delete_permission(fileId: str, permissionId: str):
        service.permissions().delete(fileId=fileId, permissionId=permissionId)