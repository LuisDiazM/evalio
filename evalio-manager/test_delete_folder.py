#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de eliminación de carpetas en GCP Cloud Storage
"""

import os
import sys
import asyncio
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.append(str(Path(__file__).parent))

from infrastructure.logger.logger import StandardLogger
from infrastructure.storage.gcp_storage import GCPStorageRepository


async def test_delete_folder():
    """Prueba la funcionalidad de eliminación de carpetas"""
    
    # Configurar logger
    logger = StandardLogger()
    
    # Configurar storage repository
    bucket_name = os.getenv("GCP_BUCKET_NAME", "evalio-multimedia-pdn")
    storage_repo = GCPStorageRepository(logger=logger, bucket_name=bucket_name)
    
    print(f"Testing GCP Storage folder deletion with bucket: {bucket_name}")
    
    # Crear datos de prueba en una carpeta
    test_folder = "test_folder_deletion/"
    test_files = [
        f"{test_folder}file1.txt",
        f"{test_folder}file2.pdf",
        f"{test_folder}subfolder/file3.jpg"
    ]
    
    test_data = {
        "file1.txt": b"This is test file 1",
        "file2.pdf": b"This is test file 2",
        "file3.jpg": b"This is test file 3"
    }
    
    try:
        # Crear archivos de prueba
        print("Creating test files...")
        for file_path in test_files:
            file_name = file_path.split('/')[-1]
            content = test_data.get(file_name, b"Default content")
            content_type = "text/plain"
            
            if file_name.endswith('.pdf'):
                content_type = "application/pdf"
            elif file_name.endswith('.jpg'):
                content_type = "image/jpeg"
            
            result = storage_repo.upload_binary(
                binary_data=content,
                destination_blob_name=file_path,
                content_type=content_type
            )
            
            if result:
                print(f"✅ Created test file: {file_path}")
            else:
                print(f"❌ Failed to create test file: {file_path}")
                return
        
        # Verificar que los archivos existen
        print("\nVerifying files exist...")
        for file_path in test_files:
            url = storage_repo.get_file_url(file_path)
            if url:
                print(f"✅ File exists: {file_path}")
            else:
                print(f"❌ File not found: {file_path}")
        
        # Eliminar la carpeta completa
        print(f"\nDeleting folder: {test_folder}")
        if storage_repo.delete_folder(test_folder):
            print(f"✅ Folder deleted successfully: {test_folder}")
        else:
            print(f"❌ Failed to delete folder: {test_folder}")
            return
        
        # Verificar que los archivos fueron eliminados
        print("\nVerifying files were deleted...")
        for file_path in test_files:
            url = storage_repo.get_file_url(file_path)
            if url:
                print(f"❌ File still exists: {file_path}")
            else:
                print(f"✅ File deleted: {file_path}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        logger.error(f"Test error: {str(e)}")


if __name__ == "__main__":
    # Verificar variables de entorno
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        print("Please set it to the path of your GCP service account key file")
        sys.exit(1)
    
    # Ejecutar prueba
    asyncio.run(test_delete_folder()) 