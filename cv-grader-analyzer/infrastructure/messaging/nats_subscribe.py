import json
from nats.aio.client import Client as NATS
from domain.repositories.subscribe_nats import EventSubscriber
import os


class NatsSubscriber(EventSubscriber):
    def __init__(self, nc: NATS):
        self.js = nc.jetstream()

    async def subscribe(self, subject: str, callback):
        async def message_handler(msg):
            data = json.loads(msg.data.decode())
            callback(data)
            await msg.ack()
        subscribe = os.getenv("NATS_SUBSCRIBER", "cv-grader-analyzer")
        await self.js.subscribe(
            subject=subject,
            durable=subscribe,
            cb=message_handler,
        )
