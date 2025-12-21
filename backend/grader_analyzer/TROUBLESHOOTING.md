# 🔧 Troubleshooting: NATS JetStream Consumer

## Error: "cannot create queue subscription to consumer"

### Causa
El consumer fue creado **sin configuración de `deliver_group`**, y ahora estás intentando suscribirte con un `queue` parameter.

### Solución

#### Opción 1: Reset Consumer (Recomendado)

Usa el script helper para eliminar y recrear el consumer:

```bash
cd backend/grader_analyzer
uv run python reset_consumer.py
```

Luego reinicia el servicio:

```bash
uv run python -m grader_analyzer.main
```

#### Opción 2: Usando NATS CLI

```bash
# Listar consumers
nats consumer ls cv-grader-analyzer

# Eliminar consumer
nats consumer rm cv-grader-analyzer cv-grader-analyzer-consumer

# Reiniciar servicio (creará consumer con configuración correcta)
cd backend/grader_analyzer
uv run python -m grader_analyzer.main
```

#### Opción 3: Manual via Python

```python
import asyncio
from nats.aio.client import Client as NATS

async def delete_consumer():
    nc = NATS()
    await nc.connect("nats://localhost:4222")
    js = nc.jetstream()
    await js.delete_consumer("cv-grader-analyzer", "cv-grader-analyzer-consumer")
    await nc.close()
    print("Consumer deleted!")

asyncio.run(delete_consumer())
```

## Verificar Consumer Configuration

```bash
# Ver configuración del consumer
nats consumer info cv-grader-analyzer cv-grader-analyzer-consumer

# Debe mostrar:
# Delivery Group: cv-grader-analyzer-workers
# Ack Policy: Explicit
# Max Deliver: 3
```

## Logs Esperados al Iniciar

✅ **Correcto:**
```
✅ Stream 'cv-grader-analyzer' exists
✅ Consumer 'cv-grader-analyzer-consumer' created with queue group 'cv-grader-analyzer-workers'
Using MinIO storage provider
✅ running subscriber...
```

❌ **Incorrecto:**
```
nats.js.errors.Error: nats: JetStream.Error cannot create queue subscription...
```

## Reset Completo (Nuclear Option)

Si nada funciona, elimina stream y consumer completamente:

```bash
# Eliminar stream (también elimina el consumer)
nats stream rm cv-grader-analyzer

# Reiniciar servicio (recreará todo desde cero)
cd backend/grader_analyzer
uv run python -m grader_analyzer.main
```

⚠️ **Advertencia**: Esto elimina todos los mensajes pendientes en el stream.

## Prevención

Siempre crea el consumer con `deliver_group` desde el inicio:

```python
consumer_config = ConsumerConfig(
    durable_name="my-consumer",
    deliver_group="my-queue-group",  # ← CRUCIAL para queue groups
    ack_policy=AckPolicy.EXPLICIT,
)
```

## Diferencias Clave

### Sin Queue Group (❌ NO escalable)
```python
ConsumerConfig(
    durable_name="consumer"
    # Sin deliver_group
)
```
- Todas las instancias reciben TODOS los mensajes
- Duplicación de procesamiento
- No es escalable

### Con Queue Group (✅ Escalable)
```python
ConsumerConfig(
    durable_name="consumer",
    deliver_group="workers"  # ← Habilita load balancing
)
```
- Solo UNA instancia recibe cada mensaje
- Load balancing automático
- Escalable horizontalmente
