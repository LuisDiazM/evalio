import asyncio
import contextlib
import os

from dotenv import load_dotenv
from nats.aio.client import Client as NATS
from nats.js.api import AckPolicy, ConsumerConfig, DeliverPolicy
from nats.js.errors import NotFoundError

from grader_analyzer.domain.grader.repositories.exam_db_repo import ExamRepository
from grader_analyzer.domain.grader.repositories.summary_db_repo import (
    SummaryQualificationRepository,
)
from grader_analyzer.domain.grader.repositories.template_db_repo import (
    TemplateRepository,
)
from grader_analyzer.domain.grader.usecases.grader_analyzer_usecase import (
    GraderAnalyzerUsecase,
)
from grader_analyzer.infrastructure.database.mongo_imp import Mongo
from grader_analyzer.infrastructure.logger.logger import StandardLogger
from grader_analyzer.infrastructure.messaging.nats_subscriber import NatsSubscriber
from grader_analyzer.infrastructure.storage.cloud_storage_gcp import (
    GCPStorageRepository,
)
from grader_analyzer.infrastructure.storage.minio_storage import MinIOStorageRepository

logger = StandardLogger()


STREAM_NAME = "cv-grader-analyzer"
EVENT_PROCESS_EXAM = "process.exam"


def get_storage_repo():
    """
    Get the storage repository based on STORAGE_PROVIDER environment variable.
    Supported values: 'gcp' (default), 'minio'
    """
    provider = os.getenv("STORAGE_PROVIDER", "gcp").lower()

    if provider == "minio":
        logger.info("Using MinIO storage provider")
        return MinIOStorageRepository()
    elif provider == "gcp":
        logger.info("Using GCP storage provider")
        return GCPStorageRepository()
    else:
        raise ValueError(
            f"Unsupported STORAGE_PROVIDER: {provider}. Use 'gcp' or 'minio'"
        )


async def ensure_stream(js):
    """
    Ensure the JetStream stream exists and is properly configured.
    Also creates the durable consumer if it doesn't exist.
    """
    desired = {
        "name": STREAM_NAME,
        "subjects": [EVENT_PROCESS_EXAM],
        "storage": "file",
        "retention": "limits",
    }
    try:
        info = await js.stream_info(STREAM_NAME)
        logger.info(f"✅ Stream '{STREAM_NAME}' exists")
        existing_subjects = set(info.config.subjects)
        if set(desired["subjects"]) != existing_subjects:
            cfg = info.config
            cfg.subjects = desired["subjects"]
            await js.update_stream(cfg)
            logger.info(f"🔄 Stream '{STREAM_NAME}' updated.")
    except NotFoundError:
        # Stream doesn't exist → create it
        await js.add_stream(**desired)
        logger.info(f"✅ Stream '{STREAM_NAME}' created.")

    # Ensure durable consumer exists with proper configuration
    consumer_env = os.getenv("NATS_CONSUMER", "cv-grader-analyzer-consumer")
    queue_env = os.getenv("NATS_QUEUE_GROUP") or consumer_env


    consumer_name = queue_env
    desired_config = ConsumerConfig(
        durable_name=consumer_name,
        deliver_group=consumer_name,
        deliver_subject=f"{STREAM_NAME}.{consumer_name}.deliver",
        filter_subject=EVENT_PROCESS_EXAM,
        ack_policy=AckPolicy.EXPLICIT,
        deliver_policy=DeliverPolicy.ALL,
        max_deliver=3,
        ack_wait=300,
    )

    def needs_recreation(existing_config: ConsumerConfig) -> bool:
        return any(
            [
                existing_config.deliver_group != desired_config.deliver_group,
                existing_config.deliver_subject != desired_config.deliver_subject,
                existing_config.filter_subject != desired_config.filter_subject,
                existing_config.ack_policy != desired_config.ack_policy,
                existing_config.deliver_policy != desired_config.deliver_policy,
                existing_config.max_deliver != desired_config.max_deliver,
                (existing_config.ack_wait or 0) != (desired_config.ack_wait or 0),
            ]
        )

    try:
        consumer_info = await js.consumer_info(STREAM_NAME, consumer_name)
        if needs_recreation(consumer_info.config):
            await js.delete_consumer(STREAM_NAME, consumer_name)
            await js.add_consumer(STREAM_NAME, config=desired_config)
    except NotFoundError:
        await js.add_consumer(STREAM_NAME, config=desired_config)
        logger.info(f"✅ Consumer '{consumer_name}' created")

    # Clean up legacy consumer if a separate durable name was previously used
    if consumer_env != consumer_name:
        with contextlib.suppress(NotFoundError):
            await js.delete_consumer(STREAM_NAME, consumer_env)


async def main():
    load_dotenv(override=False)
    nc = NATS()
    host = os.getenv("NATS_URL", "")
    if host == "":
        raise ValueError("NATS_HOST is not set")
    await nc.connect(host)
    js = nc.jetstream()

    # Ensure stream and consumer are properly configured
    await ensure_stream(js)

    mongo_client = Mongo()
    storage_repo = get_storage_repo()
    exam_repo = ExamRepository(mongo=mongo_client)
    template_repo = TemplateRepository(mongo=mongo_client)
    summary_repo = SummaryQualificationRepository(mongo=mongo_client)
    usecase = GraderAnalyzerUsecase(
        exam_repo=exam_repo,
        temp_repo=template_repo,
        summary_repo=summary_repo,
        logger=logger,
        storage_repo=storage_repo,
    )

    subscriber = NatsSubscriber(nc)

    await subscriber.subscribe(EVENT_PROCESS_EXAM, usecase.analyze)

    logger.info("✅ running subscriber...")
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()
        await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
