import os

from google.cloud import storage

from grader_analyzer.domain.shared.storage_repo import IStorageRepository


class GCPStorageRepository(IStorageRepository):
    def __init__(self, credentials_path: str = ""):
        if credentials_path != "":
            self.client = storage.Client.from_service_account_json(credentials_path)
        else:
            self.client = storage.Client()

    def download_file(
        self, bucket_name: str, source_blob_name: str, destination_file_name: str
    ) -> str:
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
            blob.download_to_filename(destination_file_name)
            return destination_file_name
        except Exception as e:
            raise Exception(f"Error downloading file from GCP Storage: {e}") from e

    def upload_file(
        self, bucket_name: str, source_file_name: str, destination_blob_name: str
    ) -> str:
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            return destination_blob_name
        except Exception as e:
            raise Exception(f"Error uploading file to GCP Storage: {e}") from e
