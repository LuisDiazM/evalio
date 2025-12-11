#!/usr/bin/env python3
"""
Script to reset NATS JetStream consumer.
Use this when you need to recreate the consumer with new configuration.
"""
import asyncio
import os

from dotenv import load_dotenv
from nats.aio.client import Client as NATS
from nats.js.errors import NotFoundError


async def reset_consumer():
    load_dotenv(override=False)

    nc = NATS()
    host = os.getenv("NATS_URL", "nats://localhost:4222")

    print(f"🔌 Connecting to NATS at {host}...")
    await nc.connect(host)
    js = nc.jetstream()

    stream_name = "cv-grader-analyzer"
    consumer_env = os.getenv("NATS_CONSUMER", "cv-grader-analyzer-consumer")
    queue_env = os.getenv("NATS_QUEUE_GROUP") or consumer_env
    if queue_env != consumer_env:
        print(
            f"ℹ️  JetStream queue subscribers require durable and queue names to match. "
            f"Deleting consumer '{queue_env}' (overriding '{consumer_env}')."
        )

    consumer_name = queue_env

    # First check if consumer exists and show its configuration
    try:
        consumer_info = await js.consumer_info(stream_name, consumer_name)
        print(
            "📋 Current consumer config: "
            f"durable='{consumer_info.config.durable_name}', "
            f"deliver_group='{consumer_info.config.deliver_group}', "
            f"filter_subject='{consumer_info.config.filter_subject}'"
        )
    except NotFoundError:
        print(f"ℹ️  Consumer '{consumer_name}' doesn't exist")

    try:
        # Try to delete existing consumer
        await js.delete_consumer(stream_name, consumer_name)
        print(f"✅ Consumer '{consumer_name}' deleted successfully")
    except NotFoundError:
        print(f"ℹ️  Consumer '{consumer_name}' was already deleted")
    except Exception as e:
        print(f"❌ Error deleting consumer: {e}")
    finally:
        await nc.close()
        print("✅ Done! You can now restart your grader_analyzer service.")


if __name__ == "__main__":
    asyncio.run(reset_consumer())
