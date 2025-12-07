import asyncio
import os

from dotenv import load_dotenv
from nats.aio.client import Client as NATS
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

logger = StandardLogger()


STREAM_NAME = "cv-grader-analyzer"
EVENT_PROCESS_EXAM = "process.exam"


async def ensure_stream(js):
    desired = {
        "name": STREAM_NAME,
        "subjects": [EVENT_PROCESS_EXAM],
        # aquí puedes agregar más opciones: storage, retention, max_msgs, etc.
        "storage": "file",
        "retention": "limits",
    }
    try:
        info = await js.stream_info(STREAM_NAME)
        # Comparamos solo subjects por simplicidad; extiende según tus necesidades
        print(info)
        existing_subjects = set(info.config.subjects)
        if set(desired["subjects"]) != existing_subjects:
            # Actualizamos sólo la parte que cambió
            cfg = info.config
            cfg.subjects = desired["subjects"]
            await js.update_stream(cfg)
            print(f"🔄 Stream '{STREAM_NAME}' updated.")
        else:
            print(f"✅ Stream '{STREAM_NAME}' exists")
    except NotFoundError:
        # No existe → lo creamos
        await js.add_stream(**desired)
        print(f"✅ Stream '{STREAM_NAME}' created.")


async def main():
    load_dotenv(override=False)
    nc = NATS()
    host = os.getenv("NATS_URL", "")
    if host == "":
        raise ValueError("NATS_HOST is not set")
    await nc.connect(host)
    js = nc.jetstream()
    await ensure_stream(js)
    # Crear stream si no existe
    await js.add_stream(name=STREAM_NAME, subjects=[EVENT_PROCESS_EXAM])

    mongo_client = Mongo()
    storage_repo = GCPStorageRepository()
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

    print("✅ running subscriber...")
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
