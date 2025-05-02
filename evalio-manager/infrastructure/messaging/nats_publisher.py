import json
from nats.aio.client import Client as NATS
from domain.templates.repositories.nats_bus import EventPublisher
from infrastructure.messaging.const import EVENT_PROCESS_EXAM

class NatsPublisher(EventPublisher):
    def __init__(self, nc: NATS):
        self.js = nc.jetstream()

    async def publish(self, data: dict, subject:str = EVENT_PROCESS_EXAM):
        await self.js.publish(subject, json.dumps(data).encode())
