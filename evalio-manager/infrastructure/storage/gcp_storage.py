import os
from typing import Optional
from google.cloud import storage
from google.cloud.exceptions import NotFound
from domain.templates.repositories.storage_repo import IStorageRepository
from domain.templates.repositories.logger_repo import LoggerInterface


class GCPStorageRepository(IStorageRepository):
    def __init__(self, logger: LoggerInterface, bucket_name: str = "evalio-multimedia-pdn"):
        """
        Initialize GCP Storage repository
        :param logger: Logger interface for logging operations
        :param bucket_name: Name of the GCP bucket (default: evalio-multimedia-pdn)
        """
        self.logger = logger
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
            
        except Exception as e:
            self.logger.error(f"Error uploading file {file_path}: {str(e)}")
            return None

    def upload_binary(self, binary_data: bytes, destination_blob_name: str, content_type: str = "application/octet-stream") -> Optional[str]:
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
            
        except Exception as e:
            self.logger.error(f"Error uploading binary data to {destination_blob_name}: {str(e)}")
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
            self.logger.info(f"File deleted successfully: {blob_name}")
            return True
            
        except NotFound:
            self.logger.warning(f"File not found for deletion: {blob_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error deleting file {blob_name}: {str(e)}")
            return False

    def delete_folder(self, folder_path: str) -> bool:
        """
        Delete a folder and all its contents from GCP Cloud Storage
        :param folder_path: Path to the folder (e.g., "exams/group_id/template_id/")
        :return: True if successful, False otherwise
        """
        try:
            # Ensure folder path ends with '/' to match all files in the folder
            if not folder_path.endswith('/'):
                folder_path += '/'
            
            # List all blobs in the folder
            blobs = self.client.list_blobs(self.bucket_name, prefix=folder_path)
            blob_list = list(blobs)
            
            if not blob_list:
                self.logger.warning(f"No files found in folder: {folder_path}")
                return True
            
            with self.client.batch():
                # Delete all blobs in the folder
                for blob in blob_list:
                    blob.delete()
                    self.logger.info(f"Deleted file: {blob.name}")
                
                self.logger.info(f"Folder deleted successfully: {folder_path} ({len(blob_list)} files)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting folder {folder_path}: {str(e)}")
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
                self.logger.warning(f"File not found: {blob_name}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting file URL for {blob_name}: {str(e)}")
            return None

    def generate_signed_url(self, blob_name: str, expiration_hours: int = 2) -> Optional[str]:
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
                    version="v4",
                    expiration=expiration_time,
                    method="GET"
                )
                return signed_url
            else:
                self.logger.warning(f"File not found for signed URL generation: {blob_name}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error generating signed URL for {blob_name}: {str(e)}")
            return ""