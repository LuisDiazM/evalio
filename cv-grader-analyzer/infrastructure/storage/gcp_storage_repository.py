from domain.repositories.storage_repo import IStorageRepository
from google.cloud import storage
import os

class GCPStorageRepository(IStorageRepository):
    def __init__(self, credentials_path: str = None):
        if credentials_path:
            self.client = storage.Client.from_service_account_json(credentials_path)
        else:
            self.client = storage.Client()

    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> str:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
        blob.download_to_filename(destination_file_name)
        return destination_file_name

    def upload_file(self, bucket_name: str, source_file_name: str, destination_blob_name: str) -> str:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return destination_blob_name 