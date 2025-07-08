# Evalio

## 1. Introducción

### 1.1. Propósito de este documento
Documentar todo el proceso que se realizó para conseguir el producto llamado evalio, desde la necesidad que quería responder la pregunta ¿Puedo tener un sistema que califique automáticamente evaluaciones de estudiantes? hasta como esa necesidad se transformó en una solución a nivel de arquitectura de software donde se aplican patrones, microservicios, comunicación entre microservicios, seguridad e infraestructura cloud, y monitoreo.
El producto al pasar por una etapa del ciclo de vida del software su diseño e implementación estará basada en los atributos de calidad del software definidos en la ISO25000.  

### 1.2. Alcance del producto
Evalio permitirá calificar parciales o evaluaciones de opciones múltiples con única respuesta usando técnicas de OMR (Optical Mark Recognition), también permitirá administrar los diferentes grupos de estudiantes, plantillas de evaluaciones para administrar los diferentes semestres.

Su modelo de acceso se basa en suscripciones mensuales que se administrarán para su control de acceso.

### 1.3. Resumen ejecutivo
Evalio es una plataforma que usando técnicas de visión por computador ayudará a calificar evaluaciones ahorrando tiempo al docente ya que el sistema de manera automática analiza las fotos y saca los resúmenes y listados de calificación.

## 2. Visión General del Producto

### 2.1. Descripción general del sistema

### 2.3. Principales casos de uso

#### 2.3.1 Configurar los grupos, examenes
En este caso de uso el profesor crea las definiciones de los grupos, las plantillas de respuestas para repartir con los estudiantes, donde cada estudiante tendrá un código QR por evaluación que identifica el examen que está presentando.

#### 2.3.2 Subir los examenes al sistema
En este caso de uso el profesor por medio de fotos sube los examenes, no necesita llenar formularios ni nada, únicamente escanear QRs por la plataforma y subir los examenes para que evalio se encargue de calificarlos usando técnicas de OMR (Optical Mark Recognition)

#### 2.3.3 Generar reportes
El profesor podrá monitorear los estudiantes a los cuales evalio ha calificado, también podrá generar los reportes de las calificaciones indiviales y comparar lo calificado por el sistema con lo real.

#### 2.3.4 Registrarse de manera gratuita
El usuario que quiera probar evalio puede registrarse de manera gratuita, sin embargo, está pendiente manejar tema de licencias finitas

#### 2.3.5 Login con el sistema
El usuario para poder usar evalio requiere estar logueado con el sistema, de lo contrario no podrá hacer uso del mismo.

## 3. Arquitectura del Sistema

### 3.1. Vista lógica
El sistema se compone de 
![logica](/docs/logica.png)

### 3.2. Vista física
![fisica](/docs/infrastructure.png)
Evalio se compone de los siguientes recursos de infraestructura en Google Cloud Platform:
- 4 Máquinas virtuales para manejar el reverse-proxy, la base de datos NoSQL, el broker de mensajería NATS, el suscriptor al broker para procesar las imágenes el grader analyzer
- 2 buckets en cloud storage GCP
- 3 Cloud run para correr los microservicios de manera serverless
- Route53 donde se había comprado inicialmente el dominio evalio.click
- Artifac registry para subir las imagenes de docker de los microservicios
- Reglas de firewall
- VPC red privada virtual
- 1 Load balancer para conectar la carga del front
- 1 CDN para manejo de caché para distribuir contenido
- 1 DNS cloud para agregar las rutas hacia el load balancer y el backend para el reverse proxy

La infraestructura completa del proyecto se encuentra definia como IaC  usando terraform y se puede observar en el siguiente repositorio https://github.com/LuisDiazM/evalio-infrastructure

**NOTA** por temas de costos en esta configuración, se decidió compartir la máquina de NATS y mongoDB en una sóla.

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

### 3.5. Vista de implementación o despliegue
El proceso usa CI mediante pipelines de github actions que se encargan de generar las imágenes docker y subir hacia un artifact registry de GCP que fue creado mediante IaC.

Para entender el proceso de despligue se tiene el siguiente diagrama donde se separa el CI que aplica directamente hacia este repositorio llamado evalio y su función es generar las imágenes de los contenedores. Para la etapa de CD se tiene un repositorio aparte de toda la infraestructura en terraform donde se actualizan los tags de las imágenes generadas por el artifact registry para que con terraform se apliquen los cambios y por ende el despliegue.

![diagram](/docs/despliegue.png)

En GCP se creó una cuenta de servicio para que sea manejada únicamente para administrar el artifact registry (almacenamiento de contenedores) y la conexión con github actions se utilizó Workload Identity Federation (WIF), esta es una característica que ofrece ventajas respecto a métodos tradicionales como generar las claves de la cuenta de servicio y almacenarlas en secretos dentro del proyecto ya que estas claves de la manera tradicional son de larga duración, con WIF se emiten claves de corta duración (1 hora defecto) con la cuenta de servicio. El siguiente articulo explica la conexión de WIF con github https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions

A continuación se muestran los pasos seguidos para lograr la conexión WIF y github actions:

* Paso 1: Crear la Cuenta de Servicio: :a cuenta de servicio con el rol Artifact Registry Administrator. Anota su dirección de correo
  electrónico, la necesitarás más adelante. Por ejemplo: evalio-runner@tu-proyecto-gcp.iam.gserviceaccount.com.

* Paso 2: Crear un Workload Identity Pool

  Un "Pool" es un contenedor para gestionar identidades externas (como GitHub Actions).

      - Ve a la consola de Google Cloud -> IAM & Admin -> Workload Identity Federation.
      - Haz clic en Crear Pool.
      - Nombre: github-pool (o el que prefieras).
      - ID del Pool: Anota este ID.
      - Haz clic en Continuar.

* Paso 3: Añadir un Proveedor al Pool

  El "Proveedor" define qué identidad externa puede asumir roles en GCP.


      - En la página de tu Pool, haz clic en Añadir Proveedor.
      - Selecciona OpenID Connect (OIDC).
      - Nombre del Proveedor: github-provider.
      - ID del Proveedor: Anota este ID.
      - Emisor (URL): https://token.actions.githubusercontent.com
      - Audiencia: Deja la audiencia por defecto (https://iam.googleapis.com/...).
      - Mapeo de Atributos:
        * google.subject: assertion.sub
        * attribute.actor: assertion.actor
        * attribute.repository: assertion.repository
      - Condición de Atributo (Opcional pero recomendado): Para limitar qué repositorios pueden usar esta identidad.
        * attribute.repository == 'tu-usuario-github/tu-repositorio'
        * Ejemplo: attribute.repository == 'LuisDiazM/evalio' # este es el repositorio
      - Haz clic en Guardar.

* Paso 4: Conceder Permisos a la Identidad Federada


  Ahora, permite que las identidades de GitHub Actions (filtradas por tu repositorio) actúen como tu cuenta de
  servicio.


   1. Ve a la página de tu Cuenta de Servicio en IAM.
   2. Selecciona la pestaña Permisos.
   3. Haz clic en Conceder Acceso.
   4. En el campo Nuevos principales, pega lo siguiente, reemplazando los valores:
    
     principalSet://iam.googleapis.com/projects/NUMERO_DE_PROYECTO/locations/global/workloadIdentityPools/ID
     _DEL_POOL/attribute.repository/tu-usuario-github/tu-repositorio


       * NUMERO\_DE\_PROYECTO: Lo encuentras en la página principal de tu proyecto de GCP.
       * ID\_DEL\_POOL: El que anotaste en el Paso 2.
       * tu-usuario-github/tu-repositorio: El nombre de tu repositorio.

   5. Asigna el rol Workload Identity User. Esto permite a la identidad federada obtener tokens para la cuenta de
      servicio.
   6. Haz clic en Guardar.
* Paso 5: Configurar los Secretos en GitHub


  Ve a tu repositorio de GitHub -> Settings -> Secrets and variables -> Actions.

  Crea los siguientes secretos:


   * GCP_WORKLOAD_IDENTITY_PROVIDER:
       * Valor:
         projects/NUMERO_DE_PROYECTO/locations/global/workloadIdentityPools/ID_DEL_POOL/providers/ID_DEL_PROVEEDOR
       * Reemplaza los valores con los que anotaste.


   * GCP_SERVICE_ACCOUNT_EMAIL:
       * Valor: El email de tu cuenta de servicio.
       * Ejemplo: evalio-runner@tu-proyecto-gcp.iam.gserviceaccount.com

   * GCP_PROJECT_ID:
       * Valor: El ID de tu proyecto de Google Cloud.


   * GCP_ARTIFACT_REGISTRY_LOCATION:
       * Valor: La región de tu Artifact Registry.
       * Ejemplo: us-central1

Adicionalmente el pipeline de despliegue cambiará los certificados ya que estos se proveen en el 
repositorio para temas de correr en local, pero para correr en cloud es importante tener otros certificados

### 3.6. Vista de datos
#### 3.6.1 Diagrama
#### 3.6.2 Modelo de datos principal.
#### 3.6.3 Catalogo
Base de datos, documentos y esquema de almacenamiento.

## 4. Tecnologías y Herramientas

### 4.1. Catalogo Stack tecnológico, Frameworks utilizados,
Dependencias externas (bibliotecas y servicios externos)

El stack tecnológico de evalio es:
* Python maneja el core de la aplicación incluyendo el procesamiento de imágenes
* Golang maneja la administración de usuarios y forward-auth para validación de identidad
* Front en react como un SPA para la interfaz con el usuario
* Base de datos NoSQL como MongoDB
* Broker de mensajería NATS
* Almacenamiento de multimedia en un storage tipo cloud storage

## 5. Seguridad

### 5.1. Modelo de seguridad de componentes involucrados.

Toda la infraestructura de evalio está dentro de una VPC de google cloud donde tiene reglas de firewall que bloquean el acceso a internet.

Las bases de datos, brokers de momento estarán dentro de la red interna sin acceso a internet.

El acceso a los microservicios únicamente está por el reverse proxy donde por medio del patrón forward-auth se valida la identidad y validación criptográfica de tokens JWT.

Los tokens JWT que firma el sistema tienen una firma asimétrica usando RSA.

El reverse proxy tiene definidos middleware para temas de rate limit.

Las contraseñas almacenadas no se guardan en texto plano sino por medio de hash criptográfico.

## 6. Integraciones y Comunicaciones Externas

Evalio de momento no expone APIS para su uso público y no se conecta con sistemas de infraestructura externos que se encuentren fuera de GCP


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

## 11. Correr localmente

Debido a que el objetivo principal es poder usar la cámara del navegador 

Como requisito debería tener docker instalado, también una herramienta
para autofirmar certificados SSL (para correr el sistema en una red interna)

Generar el certificado para su dirección IP o si puede exponer un servidor dns dentro de la red interna donde va "\<IP>" reemplaza el valor

```bash
openssl req -x509 -newkey rsa:4096 -keyout traefik.key -out traefik.crt -days 365 -nodes -subj "/CN=<IP>"
```

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```

## Anexos
### Definición de tareas

✅ Definir requisitos del sistema que se convertirán en casos de uso

✅ Definir los procesos que tiene el sistema

✅ Diseñar la solución como vista lógica de componentes

✅ Diseñar los modelos de datos de la solución

✅ Crear el boilerplate de los componentes de la vista lógica

1. ✅ Trabajar el servicio princial de manera jerarquica a nivel de dominios y exponer APIS

    ✅ grupos

    ✅ plantillas de hojas de respuestas

    ✅ examenes de los estudiantes

    ✅ generador de resumenes de calificaciones

2. ✅ Trabajar en el servicio que se encarga de analizar imágenes por OMR
    estudiar la teoría, pipeline para procesar imagenes y definición y ajuste del proceso

3. ✅ Comunicar el servicio general con el que analiza imágenes

4. ✅ Diseñar como sería la experiencia de usuario con base a los procesos definidos
5. ✅ Trabajar en el front Diseñando su interfaz con mocks de datos
6. ✅ Conectar el front con el backend

✅ Crear los contenedores de los servicios

✅ Administrar los contenedores mediante un docker compose de manera local

✅ compartir el volumen entre los ms para gestionar examenes subidos

✅ agregar traefik como reverse proxy

✅ agregar traefik con ssl autofirmado red local 

✅ agregar docker del front (por temas de pruebas)

✅ capturar fotos desde la app corriendo por contenedores

✅ empezar a ajustar el grader analyzer con las fotos reales

✅ Crear el servicio de administración de usuarios golang fiber, CRUD completo incluido login, registro (rutas públicas) duración finita de suscripción

✅ Crear el servicio de forwardAuth para validar los token de acceso

✅ Integrar servicio usuarios y forwardAuth con traefik

✅ Agregar login y registro de usuario interactuando el back y el front

✅ implementar storage GCP dentro del código y firmar urls

✅ Diseñar la infraestructura en el cloud seleccionado GCP

✅  En el front mostrar la evaluación detectada por el sistema

✅ Crear el pipeline en github actions

✅ Definir el artifact registry para las imagenes en terraform


* Definir la infraestructura como código usando terraform parte por parte

* Ajustar infraestructura y probar APP
* Definir como monitorear el sistema que herramientas se usarán
* Unificar logs

Mejoras para el sistema:
* Hay estudiantes que se retiran, al generar parciales esas hojas se pierden
* En la lista de parciales mostrar información del grupo
* En las hojas que se imprimen de respuestas colocar el nombre del grupo
* Agregar navegación hacia atrás y mejorar estilos

### Videos del sistema