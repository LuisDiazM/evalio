# Evalio

### 1 Alcance del producto

Evalio permitirá calificar parciales o evaluaciones de opciones múltiples con única respuesta usando técnicas de OMR (Optical Mark Recognition), también permitirá administrar los diferentes grupos de estudiantes, plantillas de evaluaciones para administrar los diferentes semestres. La calificación consiste en detectar las respuestas y compararlas con un patrón que se carga desde la plataforma.

## 2. Visión General del Producto

### 2.1. Requisitos

#### 2.1.1 Requisitos funcionales

- Permitir cargar las fotos de las evaluaciones mediante una interfaz web ya que el docente inicialmente subirá las fotos tomadas con su celular.
- Identificar automáticamente el estudiante al momento de subir la foto de su evaluación.
- Un profesor puede tener diferentes grupos de estudiantes donde por periodo académico puede realizar hasta 4 evaluaciones o parciales por semestre.
- Identificar las respuestas de los estudiantes mediante técnicas de visión por computador.
- Comparar con un patrón las respuestas de los estudiantes para obtener la calificación.
- El sistema debe generar un reporte de los resultados de las pruebas por grupo y evaluación calificada por el sistema como la imagen con las respuestas detectadas.
- Exportar los datos de los estudiantes en un csv donde cada estudiante identificado tenga su nota.

#### 2.1.2 Requisitos no funcionales

- Tener un mecanismo de autenticación (puede ser básico) si guarda contraseñas debe encriptar con mecanismos seguros.
- Un profesor no puede acceder o modificar a información de otro profesor.
- Los datos deben tener un ciclo de vida, es decir, no se debe permitir generar datos residuales, por ejemplo: que se elimine una evaluación de base de datos y no del storage.
- El procesamiento de imágenes no debe afectar la navegación por la plataforma, es decir, si está procesando concurrentemente 50 examenes estos no deberían afectar el rendimiento del sistema.

### 2.2 Vista de procesos

#### 2.2.0 Registro y acceso del sistema

Dado que la aplicación va a estar desplegada no se puede tener una aplicación
sin control de usuarios porque podrían mezclarse los datos de diferentes profesores, para ello un usuario nuevo se debe registrar para poder acceder donde el sistema de control de usuarios pueda validar usuarios y permitir el uso del sistema siempre y cuando esté autenticado, con el control de usuarios es posible tener una arquitectura multitenant que comparte la misma infraestructura pero que los datos tienen una segmentación lógica que permite su independencia.

#### 2.2.1 Configuraciones para el calificador

Este proceso se puede describir como:

- El profesor debe crear el grupo de estudiantes para tener la información de referencia, para evitar subir estudiante por estudiante su información el profesor puede subir un csv con la información de todos los estudiantes, y datos del grupo.
- El profesor debe subir la plantilla de respuestas de la prueba, es decir, cada pregunta con su respectiva respuesta A,B,C o D ya que esta plantila será tomada como referencia para las calificaciones.
- Con la información del grupo creada y la plantilla de respuestas es posible generar las hojas de respuestas que es un PDF con la información de los estudiantes codificada en QR y la plantilla de los ovalos de selección múltiple con única respuesta. Para optimizar el proceso de impresión por cada hoja tamaño carta se puede tener la información de 3 estudiantes.

#### 2.2.2 Subir una prueba al sistema para calificar

Este proceso consiste en tomar cada prueba del estudiante y subirla al sistema, este proceso se puede describir como:

- El profesor toma una foto de la hoja de respuestas por la plataforma, donde el sistema lee el código QR del estudiante.
- El sistema con la información del estudiante decodificada del QR se segmenta la imagen únicamente con las respuestas donde por medio de un cliente HTTP se sube la información al backend.
- El backend se encargará de recibir la información y subirla hacia un storage que puede ser cloud o local (carpeta)
- El backend cuando tiene los recursos listos publicará un evento asincrono para que el servicio encargado del OMR (optical mark recognition) realice la calificación automática del examen.
- Se guarda un registro del examen que se subió junto con el estado de la calificación.

#### 2.2.3 Analizar una prueba

El servicio que procesa las imágenes recibe la petición con el identificador del examen y deberá obtener las respuestas del estudiante y compararlas con la plantilla para generar la calificación que tendrá el estudiante y que será usada en los reportes de grupo, también deberá actualizar el estado de la calificación.

#### 2.2.4 Descarga del consolidado de resultados

El profesor podrá descargar el reporte consolidado en formato csv para que pueda ser leido por excel y gestionar
las notas de los estudiantes, adicional a ello podrá ver la información de cada estudiante y las respuestas de los estudiantes
junto con lo que detectó el sistema señalado en la imagen que subió para su calificación

#### 2.2.5 El profesor podrá eliminar la información

El profesor podrá eliminar la información de los grupos o las plantillas de respuestas donde el sistema deberá eliminar toda información relacionada para evitar los residuos que en volumenes altos generan costos innecesarios.

## 3. Arquitectura del Sistema

### 3.1. Vista lógica

El sistema se compone de:

- 1 microservicio que será un servidor web para la administración de la plataforma como configuraciones de grupos, generación de reportes, configuraciones de plantillas de respuestas, este servicio se llamará backend/admin.
- 1 microservicio que será un servidor web encargado de la gestión de usuarios donde permitirá crear, validar, generar tokens de acceso de los usuarios del sistema, se llamará backend/usersManager.
- 1 microservicio encargado del procesamiento de las imágenes donde aplicará las tecnicas de visión por computador y generará la calificación del estudiante, este servicio debe ser asincrono donde será un suscriptor a una cola de un broker de mensajería, se llamará backend/grader_analyzer.
- 1 microservicio que será un servidor web encargado de la autenticación ya que se planea implementar el patrón forward auth donde esa responsabilidad se le delega a un único servicio y así los demás microservicios mantienen sus responsabilidades, se llamará backend/forwardAuth
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

La infraestructura completa del proyecto se encuentra definia como IaC dentro de la carpeta llamada terraform
**NOTA** por temas de costos en esta configuración, se decidió compartir la máquina de NATS y mongoDB en una sóla.

### 3.4. Vista de desarrollo

El proyecto es un monorepositorio que se gestiona con Nx donde viven las apps tanto del backend como del front en un mismo lugar, su estructura general es la siguiente:

```
apps
  evalio-ui
    src
      app
        config
        features
          feature
            pages
            services
            components
            utils
        i18n
        shared
        styles
        app.tsx
backend
  admin
    domain
    infrastructure
    main.py
  forwardAuth
    ...
  grader_analyzer
    ...
  usersManager
    domain
    infrastructure
    main.go
configs
  certs
```

Cada microservicio busca implementar una clean architecture donde la etapa de negocio no dependa de capas de infraestructura y todo se maneja por medio de interfaces e inyección de dependencias.

### 3.5. Vista de implementación o despliegue

El proceso usa CI mediante pipelines de github actions que se encargan de generar las imágenes docker y subir hacia un artifact registry de GCP que fue creado mediante IaC.

Para entender el proceso de despligue se tiene el siguiente diagrama donde se separa el CI que aplica directamente hacia este repositorio llamado evalio y su función es generar las imágenes de los contenedores. Para la etapa de CD se tiene un repositorio aparte de toda la infraestructura en terraform donde se actualizan los tags de las imágenes generadas por el artifact registry para que con terraform se apliquen los cambios y por ende el despliegue.

![diagram](/docs/despliegue.png)
Al final la estrategia completa no se implementó porque se quería dejar todo en un solo lugar, es decir, el CD no se hizo automático sino subiendo las imágenes directamente al artifact registry con docker push y modificando en terraform la versión para desplegar con terraform apply.

En GCP se creó una cuenta de servicio para que sea manejada únicamente para administrar el artifact registry (almacenamiento de contenedores) y la conexión con github actions se utilizó Workload Identity Federation (WIF), esta es una característica que ofrece ventajas respecto a métodos tradicionales como generar las claves de la cuenta de servicio y almacenarlas en secretos dentro del proyecto ya que estas claves de la manera tradicional son de larga duración, con WIF se emiten claves de corta duración (1 hora defecto) con la cuenta de servicio. El siguiente articulo explica la conexión de WIF con github https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions

A continuación se muestran los pasos seguidos para lograr la conexión WIF y github actions:

- Paso 1: Crear la Cuenta de Servicio: :a cuenta de servicio con el rol Artifact Registry Administrator. Anota su dirección de correo
  electrónico, la necesitarás más adelante. Por ejemplo: evalio-runner@tu-proyecto-gcp.iam.gserviceaccount.com.

- Paso 2: Crear un Workload Identity Pool

  Un "Pool" es un contenedor para gestionar identidades externas (como GitHub Actions).

      - Ve a la consola de Google Cloud -> IAM & Admin -> Workload Identity Federation.
      - Haz clic en Crear Pool.
      - Nombre: github-pool (o el que prefieras).
      - ID del Pool: Anota este ID.
      - Haz clic en Continuar.

- Paso 3: Añadir un Proveedor al Pool

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

- Paso 4: Conceder Permisos a la Identidad Federada

  Ahora, permite que las identidades de GitHub Actions (filtradas por tu repositorio) actúen como tu cuenta de
  servicio.

  1.  Ve a la página de tu Cuenta de Servicio en IAM.
  2.  Selecciona la pestaña Permisos.
  3.  Haz clic en Conceder Acceso.
  4.  En el campo Nuevos principales, pega lo siguiente, reemplazando los valores:

  principalSet://iam.googleapis.com/projects/NUMERO_DE_PROYECTO/locations/global/workloadIdentityPools/ID
  \_DEL_POOL/attribute.repository/tu-usuario-github/tu-repositorio

       * NUMERO\_DE\_PROYECTO: Lo encuentras en la página principal de tu proyecto de GCP.
       * ID\_DEL\_POOL: El que anotaste en el Paso 2.
       * tu-usuario-github/tu-repositorio: El nombre de tu repositorio.

  5.  Asigna el rol Workload Identity User. Esto permite a la identidad federada obtener tokens para la cuenta de
      servicio.
  6.  Haz clic en Guardar.

- Paso 5: Configurar los Secretos en GitHub

  Ve a tu repositorio de GitHub -> Settings -> Secrets and variables -> Actions.

  Crea los siguientes secretos:

  - GCP_WORKLOAD_IDENTITY_PROVIDER:

    - Valor:
      projects/NUMERO_DE_PROYECTO/locations/global/workloadIdentityPools/ID_DEL_POOL/providers/ID_DEL_PROVEEDOR
    - Reemplaza los valores con los que anotaste.

  - GCP_SERVICE_ACCOUNT_EMAIL:

    - Valor: El email de tu cuenta de servicio.
    - Ejemplo: evalio-runner@tu-proyecto-gcp.iam.gserviceaccount.com

  - GCP_PROJECT_ID:

    - Valor: El ID de tu proyecto de Google Cloud.

  - GCP_ARTIFACT_REGISTRY_LOCATION:
    - Valor: La región de tu Artifact Registry.
    - Ejemplo: us-central1


### 3.6. Vista de datos

#### 3.6.1 Diagrama

Las entidades identificadas durante el proceso son:

![manager](/docs/evalio-manager.jpg)
![users](/docs/evalio-users.jpg)

Cargas de trabajo:

Operaciones de lectura:

- Listar los grupos por profesor
- Listar las plantillas de respuestas por grupo
- Obtener los resumen de calificaciones por evaluacion dentro de un grupo

Operaciones de escritura:

- Crear un profesor
- Crear un grupo
- Crear una plantilla de respuestas
- Crear un resumen de calificaciones
- Actualizar un resumen de calificaciones
- Actualizar el estado de procesamiento de un examen

Operaciones de eliminación

- Eliminar un grupo

#### 3.6.2 Relaciones de entidades

Para los grupos la información de estudiantes se elige como embedding ya que los estudiantes no van a cambiar o sus identificaciones. Con los profesores tienen una relación por referencia professor_id

Los examenes tienen relacion por referencia con los grupos, es decir, tienen un campo de group_id

Las plantillas de respuestas tienen relación por referencia con los grupos y profesores.

Los resumen de calificaciones tiene las calificaciones obtenidas por los estudiantes mediante embeddings este patrón de diseño se llama compute donde se genera el reporte en un único documento así al obtener las calificaciones consolidadas no requiere de queries y relaciones complejas.

## 4. Tecnologías y Herramientas

### 4.1. Catalogo Stack tecnológico, Frameworks utilizados,

Dependencias externas (bibliotecas y servicios externos)

El stack tecnológico de evalio es:

- Python maneja el core de la aplicación incluyendo el procesamiento de imágenes
- Golang maneja la administración de usuarios y forward-auth para validación de identidad
- Front en react como un SPA para la interfaz con el usuario
- Base de datos NoSQL como MongoDB
- Broker de mensajería NATS
- Almacenamiento de multimedia en un storage tipo cloud storage
- Nube usada GCP, los microservicios todos corren en contenedores para transportabilidad y evolución de infraestructura.

## 5. Seguridad

### 5.1. Modelo de seguridad de componentes involucrados.

Toda la infraestructura de evalio está dentro de una VPC de google cloud donde tiene reglas de firewall que bloquean el acceso a internet.

Las bases de datos, brokers de momento estarán dentro de la red interna sin acceso a internet.

El acceso a los microservicios únicamente está por el reverse proxy donde por medio del patrón forward-auth se valida la identidad y validación criptográfica de tokens JWT.

Los tokens JWT que firma el sistema tienen una firma asimétrica usando RSA.

El reverse proxy tiene definidos middleware para temas de rate limit.

Las contraseñas almacenadas no se guardan en texto plano sino por medio de hash criptográfico.

## 6. Integraciones y Comunicaciones Externas

Evalio de momento no expone APIS para su uso público y no se conecta con sistemas de infraestructura externos que se encuentren fuera de GCP, las APIS de acceso del sistema están publicadas con el mecanismo de seguridad que usa evalio por JWT firmados con RSA, sin embargo, no están pensadas para exponer a otros sistemas externos de momento.

## 7. Escalabilidad y Rendimiento

### 7.1. Descripción de procesos de escalamiento.

Actualmente evalio cuenta con 3 microservicios serverless con cloud run cuyo escalamiento es automático por GCP basado en req/s y uso de CPU, 1 máquina virtual que ejecuta el microservicio que analyza las imágenes, sin embargo, este microservicio hace pull 1 examen a la vez, lo que en teoría sacrifica tiempo para no estar sesgado en recursos, si se quisiera reducir el tiempo se podría escalar horizontalmente este servicio (de momento no lo hace), para la base de datos y el broker que conviven en la misma máquina (por temas de costos) el escalamiento sería manual y de forma vertical.

## 8. Operación y Mantenimiento

### 8.1. Estrategias de monitoreo

Dado que la aplicación de evalio no va a estar corriendo por mucho tiempo o que sea un producto, no se tiene implementada una estrategia, sin embargo, como temas practicos se estudiará la viabilidad de prometheus + grafana.

### 8.2. Gestión de logs y alertas

Los logs no se tiene estrategia de estandard implementada, pero como temas practicos se estudiará fluentd como mecanismo de centralización.

## 9. Decisiones Arquitectónicas Clave

### 9.1. Registro de decisiones arquitectónicas (ADR)

- El proyecto escogió la arquitectura entre servicios serverless y máquinas virtuales gestionadas con herramientas opensource que
  se pudiesen instalar como docker, traefik, nats, mongodb, esto se hace con el fin de tener los menores costos posibles.

- La distribución del front, hay otras alternativas para exponerlo especialmente para una aplicación de bajo tráfico como evalio, sin embargo, se escogío esta arquitectura con el balanceador de carga, CDN, bucket porque es la arquitectura más robusta para exponer un front y a nivel personal me permitía practicar.

- El análisis por OMR tuvo varias fases iniciando con detección de bordes, detección de formas, incluso con el entrenamiento de un red neuronal convolucional, sin embargo, la que mejor tuvo éxito fue la mezcla entre detección de bordes y formas.

- ¿Por qué hay un dominio en amazon y la infraestructura en GCP? el dominio lo había comprado antes de que surgiera la idea, la compra fue con fines de práctica y cuando surgió la idea se decidió llamar el proyecto basado en el dominio previamente adquirido, por eso está en ruta53 y no en GCP.

### 9.2. Impactos de las decisiones tomadas

- El proyecto es más una práctica basado en una pasión personal y se llevó al punto de hacerlo lo más parecido a un producto completo que cubriera el ciclo de vida de desarrollo del software.

- También se quiere explorar el uso de LLMs para tareas de clasificación y probar su eficacia costo/beneficio, esto podrá expandir los tipos de respuestas ya que actualmente sólo está limitado a 4 opciones de respuesta A,B,C o D.
