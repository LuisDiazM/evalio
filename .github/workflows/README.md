# GitHub Actions Workflows

Este directorio contiene los workflows de GitHub Actions para automatizar el build y deployment de las imágenes Docker.

## Workflows Disponibles

### 1. `build-users-manager.yml`
**Propósito**: Build y push de la imagen Docker del servicio `users-manager`

**Triggers**:
- Push a la rama `develop` (solo si hay cambios en `users-manager/`)
- Pull Request a la rama `develop` (solo si hay cambios en `users-manager/`)

**Acciones**:
- Build de la imagen Docker
- Push a GitHub Container Registry (ghcr.io)
- Generación automática de tags basados en branch y commit

### 2. `build-users-manager-test.yml`
**Propósito**: Testing del build de la imagen Docker del servicio `users-manager`

**Triggers**: Mismos que el workflow principal

**Acciones**:
- Build de la imagen Docker (sin push)
- Validación de que la imagen se construye correctamente

### 3. `template-docker-build.yml`
**Propósito**: Template reutilizable para otros servicios

**Uso**: Configurar variables de repositorio en GitHub:
- `SERVICE_NAME`: Nombre del servicio (ej: "cv-grader-analyzer")
- `SERVICE_PATH`: Ruta del directorio del servicio (ej: "cv-grader-analyzer")

## Configuración Requerida

### 1. Permisos de Repositorio
Asegúrate de que el repositorio tenga habilitados los siguientes permisos:
- **Actions**: Read and write permissions
- **Packages**: Read and write permissions

### 2. Variables de Repositorio (para el template)
Si usas el template, configura estas variables en Settings > Secrets and variables > Actions > Variables:

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SERVICE_NAME` | Nombre del servicio para la imagen | `cv-grader-analyzer` |
| `SERVICE_PATH` | Ruta del directorio del servicio | `cv-grader-analyzer` |

## Tags Generados

Los workflows generan automáticamente los siguientes tags:

- `develop`: Para builds de la rama develop
- `pr-{number}`: Para pull requests
- `develop-{sha}`: Para commits específicos en develop
- `latest`: Solo para la rama principal (main/master)

## Ejemplo de Uso

### Para el servicio users-manager:
El workflow ya está configurado y se ejecutará automáticamente cuando hagas push a `develop`.

### Para otros servicios usando el template:
1. Copia el archivo `template-docker-build.yml`
2. Renómbralo según tu servicio (ej: `build-cv-grader.yml`)
3. Configura las variables de repositorio
4. El workflow se ejecutará automáticamente

## Monitoreo

Puedes monitorear la ejecución de los workflows en:
- **Actions tab** de tu repositorio GitHub
- **Packages tab** para ver las imágenes publicadas

## Troubleshooting

### Error de permisos:
- Verifica que el repositorio tenga permisos de Packages habilitados
- Asegúrate de que `GITHUB_TOKEN` esté disponible

### Error de build:
- Verifica que el Dockerfile esté en la ruta correcta
- Revisa los logs del workflow para detalles específicos

### Imagen no se publica:
- Verifica que no sea un Pull Request (las PRs solo hacen build, no push)
- Confirma que estés en la rama `develop` 