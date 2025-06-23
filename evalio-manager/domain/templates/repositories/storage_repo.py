from abc import ABC, abstractmethod
from typing import Optional


class IStorageRepository(ABC):
    @abstractmethod
    def upload_file(self, file_path: str, destination_blob_name: str) -> Optional[str]:
        """
        Upload a file to cloud storage
        :param file_path: Local path to the file
        :param destination_blob_name: Name for the file in cloud storage
        :return: Public URL of the uploaded file or None if failed
        """
        pass

    @abstractmethod
    def upload_binary(self, binary_data: bytes, destination_blob_name: str, content_type: str = "application/octet-stream") -> Optional[str]:
        """
        Upload binary data to cloud storage
        :param binary_data: Binary data to upload
        :param destination_blob_name: Name for the file in cloud storage
        :param content_type: MIME type of the file
        :return: Public URL of the uploaded file or None if failed
        """
        pass

    @abstractmethod
    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from cloud storage
        :param blob_name: Name of the file in cloud storage
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_folder(self, folder_path: str) -> bool:
        """
        Delete a folder and all its contents from cloud storage
        :param folder_path: Path to the folder (e.g., "exams/group_id/template_id/")
        :return: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_file_url(self, blob_name: str) -> Optional[str]:
        """
        Get the public URL of a file in cloud storage
        :param blob_name: Name of the file in cloud storage
        :return: Public URL or None if file doesn't exist
        """
        pass

    @abstractmethod
    def generate_signed_url(self, blob_name: str, expiration_hours: int = 2) -> Optional[str]:
        """
        Generate a signed URL for a file in cloud storage
        :param blob_name: Name of the file in cloud storage
        :param expiration_hours: Number of hours until the URL expires (default: 2)
        :return: Signed URL or None if file doesn't exist
        """
        pass 