# Configuración de GCP Cloud Storage

## Variables de Entorno Requeridas

Para usar el almacenamiento en la nube de GCP, necesitas configurar las siguientes variables de entorno:

```bash
# Environment
ENVIRONMENT=production

# GCP Configuration
GCP_BUCKET_NAME=evalio-multimedia-pdn
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

# NATS Configuration
NATS_URL=nats://localhost:4222

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
```

## Configuración de GCP

### 1. Crear un proyecto en Google Cloud Platform

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la API de Cloud Storage

### 2. Crear un bucket de almacenamiento

1. Ve a Cloud Storage en la consola de GCP
2. Crea un nuevo bucket con el nombre `evalio-multimedia-pdn`
3. Configura el bucket como público (si necesitas acceso público a los archivos)

### 3. Crear una cuenta de servicio

1. Ve a IAM & Admin > Service Accounts
2. Crea una nueva cuenta de servicio
3. Asigna los siguientes roles:
   - Storage Object Admin
   - Storage Object Viewer
4. Descarga la clave JSON de la cuenta de servicio

### 4. Configurar las credenciales

1. Guarda el archivo JSON de la cuenta de servicio en tu servidor
2. Configura la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` con la ruta al archivo

## Estructura de Archivos en Cloud Storage

Los archivos se organizarán en el bucket con la siguiente estructura:

```
exams/
├── group_id_1/
│   ├── template_id_1/
│   │   ├── student_123.pdf
│   │   └── student_456.jpg
│   └── template_id_2/
│       └── student_789.png
└── group_id_2/
    └── template_id_3/
        └── student_111.pdf
```

## Funcionalidades Implementadas

### 1. Subida de Archivos
- **Subida desde archivo local**: `upload_file()`
- **Subida de datos binarios**: `upload_binary()`
- **Detección automática de tipo de archivo**
- **Generación de nombres únicos**

### 2. Eliminación de Archivos
- **Eliminación de archivo individual**: `delete_file()`
- **Eliminación de carpeta completa**: `delete_folder()`

### 3. Gestión de Templates
- **Eliminación automática**: Cuando se elimina un template, se eliminan automáticamente:
  - Todos los exámenes asociados en la base de datos
  - Toda la carpeta del template en cloud storage (`exams/{group_id}/{template_id}/`)

## Uso

### Modo Local
Cuando `ENVIRONMENT=local`, los archivos se mantienen en el sistema de archivos local.

### Modo Producción
Cuando `ENVIRONMENT=production`, los archivos se suben automáticamente a GCP Cloud Storage.

### Datos de Entrada

El sistema acepta dos tipos de entrada para los archivos:

1. **Ruta de archivo local**: `exam_path`
2. **Datos binarios**: `exam_binary`

Ejemplo de datos de entrada:

```python
exam_data = {
    "student_identification": "12345",
    "template_id": "template_001",
    "group_id": "group_001",
    "student_name": "Juan Pérez",
    "exam_path": "/path/to/local/file.pdf",  # Para archivo local
    # O
    "exam_binary": binary_data,  # Para datos binarios
}
```

## API Endpoints

### POST /exam
- **Funcionalidad**: Crear un nuevo examen
- **Archivo**: Subido como `UploadFile`
- **Modo Local**: Guarda archivo temporalmente
- **Modo Producción**: Sube directamente a cloud storage

### GET /exams
- **Funcionalidad**: Obtener exámenes por template
- **Retorna**: Lista de exámenes con URLs de cloud storage

### DELETE /template/{template_id}
- **Funcionalidad**: Eliminar template y todos sus archivos asociados
- **Acciones**:
  - Elimina template de la base de datos
  - Elimina todos los exámenes asociados
  - Elimina toda la carpeta del template en cloud storage

## Pruebas

### Script de Prueba de Eliminación de Carpetas
Ejecutar `test_delete_folder.py` para verificar la funcionalidad de eliminación:

```bash
python test_delete_folder.py
```

### Verificaciones
- ✅ Creación de archivos de prueba
- ✅ Verificación de existencia
- ✅ Eliminación de carpeta completa
- ✅ Verificación de eliminación
- ✅ Manejo de errores

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

La dependencia `google-cloud-storage==2.14.0` ya está incluida en el archivo `requirements.txt`.

## Seguridad

### Permisos de GCP
La cuenta de servicio necesita los siguientes roles:
- `Storage Object Admin` (para crear, actualizar y eliminar archivos)
- `Storage Object Viewer` (para leer archivos)

### Configuración del Bucket
- Los archivos se hacen públicos automáticamente
- Considerar configurar CORS si es necesario
- Implementar políticas de retención según necesidades

## Monitoreo

### Logs
Todas las operaciones se registran usando el logger configurado:
- Subidas exitosas
- Eliminaciones de archivos y carpetas
- Errores de operaciones
- URLs generadas

### Métricas Recomendadas
- Tiempo de subida
- Tiempo de eliminación
- Tasa de éxito
- Uso de almacenamiento
- Costos de transferencia 