import asyncio
from nats.aio.client import Client as NATS
from infrastructure.messaging.nats_publisher import NatsPublisher
import json
import os

STREAM_NAME = "cv-grader-analyzer"
EVENT_PROCESS_EXAM = "process.exam"
async def run():
    nc = NATS()
    host = os.getenv("NATS_URL", "nats://localhost:4222")
    await nc.connect(host)
    js = nc.jetstream()

    await js.add_stream(name=STREAM_NAME, subjects=[EVENT_PROCESS_EXAM])
    publisher = NatsPublisher(nc)
    await publisher.publish(EVENT_PROCESS_EXAM, json.dumps({"exam_id": "68140659b8e60ba5859eb8a6"}))
    print("📤 published event")

if __name__ == "__main__":
    asyncio.run(run())