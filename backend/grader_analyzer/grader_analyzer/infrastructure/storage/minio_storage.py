import os

from minio import Minio
from minio.error import S3Error

from grader_analyzer.domain.shared.storage_repo import IStorageRepository


class MinIOStorageRepository(IStorageRepository):
    def __init__(self):
        """
        Initialize MinIO Storage repository for grader_analyzer
        Environment variables required:
        - MINIO_ENDPOINT: MinIO server endpoint (e.g., localhost:9000)
        - MINIO_ACCESS_KEY: Access key for MinIO
        - MINIO_SECRET_KEY: Secret key for MinIO
        - MINIO_BUCKET_NAME: Bucket name
        - MINIO_SECURE: Whether to use HTTPS (default: False)
        """
        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "evalio-multimedia")
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"

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

    def download_file(
        self, bucket_name: str, source_blob_name: str, destination_file_name: str
    ) -> str:
        """
        Download a file from MinIO and save it locally
        :param bucket_name: Bucket name (can override default)
        :param source_blob_name: Object name in MinIO
        :param destination_file_name: Local path where file will be saved
        :return: Local path of downloaded file
        """
        try:
            # Create destination directory if it doesn't exist
            os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

            # Use provided bucket or default
            bucket = bucket_name if bucket_name else self.bucket_name

            # Download file from MinIO
            self.client.fget_object(bucket, source_blob_name, destination_file_name)

            return destination_file_name
        except S3Error as e:
            raise Exception(f"Error downloading file from MinIO: {e}") from e

    def upload_file(
        self, bucket_name: str, source_file_name: str, destination_blob_name: str
    ) -> str:
        """
        Upload a local file to MinIO
        :param bucket_name: Bucket name (can override default)
        :param source_file_name: Local file path
        :param destination_blob_name: Object name in MinIO
        :return: Object name if successful
        """
        try:
            # Use provided bucket or default
            bucket = bucket_name if bucket_name else self.bucket_name

            # Upload file to MinIO
            self.client.fput_object(bucket, destination_blob_name, source_file_name)

            return destination_blob_name
        except S3Error as e:
            raise Exception(f"Error uploading file to MinIO: {e}") from e
