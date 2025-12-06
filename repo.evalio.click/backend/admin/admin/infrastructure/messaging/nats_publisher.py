import json

from nats.aio.client import Client as NATS

from admin.domain.shared.event_repo import EventPublisher

STREAM_NAME = "cv-grader-analyzer"
EVENT_PROCESS_EXAM = "process.exam"


class NatsPublisher(EventPublisher):
    def __init__(self, nc: NATS):
        self.js = nc.jetstream()

    async def publish(self, data: dict, subject: str = EVENT_PROCESS_EXAM):
        await self.js.publish(subject, json.dumps(data).encode())
