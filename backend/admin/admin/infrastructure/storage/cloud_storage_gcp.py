import os
from typing import Optional

from google.cloud import storage
from google.cloud.exceptions import NotFound

from admin.domain.shared.storage_repo import IStorageRepository


class GCPStorageRepository(IStorageRepository):
    def __init__(
        self,
    ):
        """
        Initialize GCP Storage repository
        :param logger: Logger interface for logging operations
        :param bucket_name: Name of the GCP bucket (default: evalio-multimedia-pdn)
        """
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, file_path: str, destination_blob_name: str) -> Optional[str]:
        """
        Upload a file to GCP Cloud Storage
        :param file_path: Local path to the file
        :param destination_blob_name: Name for the file in cloud storage
        :return: Public URL of the uploaded file or None if failed
        """
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(file_path)
            return destination_blob_name

        except Exception:
            return None

    def upload_binary(
        self,
        binary_data: bytes,
        destination_blob_name: str,
        content_type: str = "application/octet-stream",
    ) -> Optional[str]:
        """
        Upload binary data to GCP Cloud Storage
        :param binary_data: Binary data to upload
        :param destination_blob_name: Name for the file in cloud storage
        :param content_type: MIME type of the file
        :return: Public URL of the uploaded file or None if failed
        """
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_string(binary_data, content_type=content_type)
            return destination_blob_name

        except Exception:
            return None

    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from GCP Cloud Storage
        :param blob_name: Name of the file in cloud storage
        :return: True if successful, False otherwise
        """
        try:
            blob = self.bucket.blob(blob_name)
            blob.delete()
            return True

        except NotFound:
            return False
        except Exception:
            return False

    def delete_folder(self, folder_path: str) -> bool:
        """
        Delete a folder and all its contents from GCP Cloud Storage
        :param folder_path: Path to the folder (e.g., "exams/group_id/template_id/")
        :return: True if successful, False otherwise
        """
        try:
            # Ensure folder path ends with '/' to match all files in the folder
            if not folder_path.endswith("/"):
                folder_path += "/"

            # List all blobs in the folder
            blobs = self.client.list_blobs(self.bucket_name, prefix=folder_path)
            blob_list = list(blobs)

            if not blob_list:
                return True

            with self.client.batch():
                # Delete all blobs in the folder
                for blob in blob_list:
                    blob.delete()

            return True

        except Exception:
            return False

    def get_file_url(self, blob_name: str) -> Optional[str]:
        """
        Get the public URL of a file in GCP Cloud Storage
        :param blob_name: Name of the file in cloud storage
        :return: Public URL or None if file doesn't exist
        """
        try:
            blob = self.bucket.blob(blob_name)
            # Check if blob exists
            if blob.exists():
                return blob.public_url
            else:
                return None

        except Exception:
            return None

    def generate_signed_url(
        self, blob_name: str, expiration_hours: int = 2
    ) -> Optional[str]:
        """
        Generate a signed URL for a file in GCP Cloud Storage
        :param blob_name: Name of the file in cloud storage
        :param expiration_hours: Number of hours until the URL expires (default: 2)
        :return: Signed URL or None if file doesn't exist
        """
        try:
            blob = self.bucket.blob(blob_name)
            # Check if blob exists
            if blob.exists():
                # Generate signed URL with expiration time
                expiration_time = expiration_hours * 3600  # Convert hours to seconds
                signed_url = blob.generate_signed_url(
                    version="v4", expiration=expiration_time, method="GET"
                )
                return signed_url
            else:
                return ""

        except Exception:
            return ""
