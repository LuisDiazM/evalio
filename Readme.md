# Evalio

## 1. Introducción

### 1.1. Propósito de este documento

### 1.2. Alcance del producto

### 1.3. Resumen ejecutivo

## 2. Visión General del Producto

### 2.1. Descripción general del sistema

### 2.3. Principales casos de uso

## 3. Arquitectura del Sistema

### 3.1. Vista lógica

### 3.2. Vista física

### 3.3. Vista de procesos

#### 3.3.0 Configuraciones para el calificador
Este proceso se puede describir como:
- El profesor debe crear el grupo de estudiantes para tener la información de referencia, para evitar el proceso 1-1 el profesor puede subir un csv con la información de los estudiantes, y datos del grupo.
- El profesor debe subir la plantilla de respuestas de la prueba, es decir, cada pregunta con su respectiva respuesta A,B,C o D
- Con la información del grupo creada y la plantilla de respuestas es posible generar las hojas de respuestas que es un PDF con la información de los estudiantes codificada en QR y la plantilla de los ovalos de selección múltiple con única respuesta. Para optimizar el proceso de impresión por cada hoja tamaño carta se puede tener la información de 3 estudiantes.

#### 3.3.1 Subir una prueba al sistema para calificar
Este proceso consiste en tomar cada prueba del estudiante y subirla al sistema, este proceso se puede describir como:
- El profesor toma una foto de la hoja de respuestas por la plataforma, donde el sistema lee el código QR del estudiante.
- El sistema con la información del estudiante decodificada del QR se segmenta la imagen únicamente con las respuestas donde por medio de un cliente HTTP se sube la información al backend.
- El backend se encargará de recibir la información y subirla hacia un storage que puede ser cloud o local (carpeta)
- El backend cuando tiene los recursos listos publicará un evento para que el servicio encargado del OMR (optical mark recognition) realice la calificación automática del examen que se aplica en 3.3.2
- Se guarda un registro del examen

#### 3.3.2 Analizar una prueba
El suscriptor del microservicio grader-analizer recibe la petición con la siguiente información:
```
{exam_id:str}
```
- Consulta en mongo el examen por el id en exams
- Descarga la prueba por el path que se envía
- Aplica el pipeline de procesamiento de imagenes
- Consulta en mongo la plantilla de respuestas por el template_id que está almacenado en el exam_id
- Compara las respuestas del OMR con las de la plantilla
- Crea el documento summary_qualifications
- Actualiza el estado del examen a completed para evitar procesarlo en el futuro

#### 3.3.3 Descarga del consolidado de resultados
El profesor podrá descargar el reporte consolidado en formato csv para que pueda ser leido por excel y gestionar
las notas de los estudiantes, adicional a ello podrá ver la información de cada estudiante y las respuestas de los estudiantes
junto con lo que detectó el sistema señalado en la imagen que subió en el proceso 3.3.1

### 3.4. Vista de desarrollo

### 3.5. Vista de implementación
### 3.6. Vista de datos
#### 3.6.1 Diagrama
#### 3.6.2 Modelo de datos principal.
#### 3.6.3 Catalogo
Base de datos, documentos y esquema de almacenamiento.

## 4. Tecnologías y Herramientas

### 4.1. Catalogo Stack tecnológico, Frameworks utilizados,
Dependencias externas (bibliotecas y servicios externos)

## 5. Seguridad

### 5.1. Modelo de seguridad de componentes involucrados.

## 6. Integraciones y Comunicaciones Externas

### 6.1. APIs expuestas e integraciones

### 6.2. Catálogo de interoperabilidades e integraciones.


## 7. Escalabilidad y Rendimiento

### 7.1. Descripción de procesos de escalamiento.

## 8. Operación y Mantenimiento

### 8.1. Estrategias de monitoreo

### 8.2. Gestión de logs y alertas


## 9. Decisiones Arquitectónicas Clave


### 9.1. Registro de decisiones arquitectónicas (ADR)

### 9.2. Impactos de las decisiones tomadas


## 10. Roadmap de Evolución

### 10.1. Características