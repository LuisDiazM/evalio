from abc import ABC, abstractmethod

class IStorageRepository(ABC):
    @abstractmethod
    def download_file(self, bucket_name: str, source_blob_name: str, destination_file_name: str) -> str:
        """
        Descarga un archivo desde un bucket de almacenamiento y lo guarda localmente.
        Retorna el path local del archivo descargado.
        """
        pass 

    @abstractmethod
    def upload_file(self, bucket_name: str, source_file_name: str, destination_blob_name: str) -> str:
        """
        Sube un archivo local al bucket y retorna el identificador del objeto en el bucket.
        """
        pass 