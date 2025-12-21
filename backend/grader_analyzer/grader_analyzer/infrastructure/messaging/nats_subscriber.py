import inspect
import json
import os

from nats.aio.client import Client as NATS

from grader_analyzer.domain.shared.event_subscriber import EventSubscriber


class NatsSubscriber(EventSubscriber):
    def __init__(self, nc: NATS):
        self.js = nc.jetstream()

    async def subscribe(self, subject: str, callback):
        """
        Subscribe to a durable consumer with queue group for load balancing.
        Multiple instances with the same durable+queue will share messages.
        """
        async def message_handler(msg):
            payload = json.loads(msg.data.decode())
            result = callback(payload)
            if inspect.isawaitable(result):
                await result
            await msg.ack()

        # Durable consumer name (shared across all instances)
        consumer_env = os.getenv("NATS_CONSUMER", "cv-grader-analyzer-consumer")
        queue_env = os.getenv("NATS_QUEUE_GROUP") or consumer_env
        consumer_name = queue_env

        # Subscribe with durable consumer and queue group
        await self.js.subscribe(
            subject=subject,
            durable=consumer_name,
            queue=consumer_name,
            cb=message_handler,
            manual_ack=True,
        )
