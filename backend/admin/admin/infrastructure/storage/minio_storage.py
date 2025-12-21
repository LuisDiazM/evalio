import os
from datetime import timedelta
from io import BytesIO
from typing import Optional

from minio import Minio
from minio.error import S3Error

from admin.domain.shared.storage_repo import IStorageRepository


class MinIOStorageRepository(IStorageRepository):
    def __init__(self):
        """
        Initialize MinIO Storage repository
        Environment variables required:
        - MINIO_ENDPOINT: MinIO server endpoint (e.g., localhost:9000)
        - MINIO_ACCESS_KEY: Access key for MinIO
        - MINIO_SECRET_KEY: Secret key for MinIO
        - MINIO_BUCKET_NAME: Bucket name
        - MINIO_SECURE: Whether to use HTTPS (default: False)
        """
        endpoint = os.getenv("MINIO_ENDPOINT")
        access_key = os.getenv("MINIO_ACCESS_KEY")
        secret_key = os.getenv("MINIO_SECRET_KEY")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "evalio-bucket")
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
        if endpoint is None or access_key is None or secret_key is None:
            raise ValueError("MinIO configuration environment variables are not set")

        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        # Create bucket if it doesn't exist
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, file_path: str, destination_blob_name: str) -> Optional[str]:
        """
        Upload a file to MinIO
        :param file_path: Local path to the file
        :param destination_blob_name: Object name in MinIO
        :return: Object name if successful, None otherwise
        """
        try:
            self.client.fput_object(
                self.bucket_name,
                destination_blob_name,
                file_path,
            )
            return destination_blob_name
        except S3Error as e:
            raise ValueError(f"Error uploading file to MinIO: {e}") from e

    def upload_binary(
        self,
        binary_data: bytes,
        destination_blob_name: str,
        content_type: str = "application/octet-stream",
    ) -> Optional[str]:
        """
        Upload binary data to MinIO
        :param binary_data: Binary data to upload
        :param destination_blob_name: Object name in MinIO
        :param content_type: MIME type of the file
        :return: Object name if successful, None otherwise
        """
        try:
            data_stream = BytesIO(binary_data)
            data_length = len(binary_data)

            self.client.put_object(
                self.bucket_name,
                destination_blob_name,
                data_stream,
                length=data_length,
                content_type=content_type,
            )
            return destination_blob_name
        except S3Error as e:
            raise ValueError(f"Error uploading binary data to MinIO: {e}") from e

    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from MinIO
        :param blob_name: Object name in MinIO
        :return: True if successful, False otherwise
        """
        try:
            self.client.remove_object(self.bucket_name, blob_name)
            return True
        except S3Error as e:
            raise ValueError(f"Error deleting file from MinIO: {e}") from e

    def delete_folder(self, folder_path: str) -> bool:
        """
        Delete a folder and all its contents from MinIO
        :param folder_path: Prefix/folder path (e.g., "exams/group_id/template_id/")
        :return: True if successful, False otherwise
        """
        try:
            # Ensure folder path ends with '/' to match all files in the folder
            if not folder_path.endswith("/"):
                folder_path += "/"

            # List all objects with the given prefix
            objects = self.client.list_objects(
                self.bucket_name, prefix=folder_path, recursive=True
            )

            # Delete all objects
            delete_errors = []
            for obj in objects:
                try:
                    if obj.object_name:
                        self.client.remove_object(self.bucket_name, obj.object_name)
                except S3Error as e:
                    delete_errors.append(str(e))

            return len(delete_errors) == 0
        except S3Error as e:
            raise ValueError(f"Error deleting folder from MinIO: {e}") from e

    def get_file_url(self, blob_name: str, expiry_seconds: int = 3600) -> Optional[str]:
        """
        Get a presigned URL for accessing a file (MinIO specific)
        :param blob_name: Object name in MinIO
        :param expiry_seconds: URL expiration time in seconds
        :return: Presigned URL or None if failed
        """
        try:
            from datetime import timedelta

            url = self.client.presigned_get_object(
                self.bucket_name, blob_name, expires=timedelta(seconds=expiry_seconds)
            )
            return url
        except S3Error as e:
            raise ValueError(f"Error generating presigned URL: {e}") from e

    def generate_signed_url(
        self, blob_name: str, expiration_hours: int = 2
    ) -> Optional[str]:
        """
        Generate a signed URL for a file (MinIO implementation)
        :param blob_name: Object name in MinIO
        :param expiration_hours: Number of hours until the URL expires
        :return: Presigned URL or None if failed
        """
        try:

            url = self.client.presigned_get_object(
                self.bucket_name,
                blob_name,
                expires=timedelta(hours=expiration_hours),
            )
            return url
        except S3Error as e:
            raise ValueError(f"Error generating signed URL: {e}") from e
