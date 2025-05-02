
import asyncio
from nats.aio.client import Client as NATS
from nats.js.errors import NotFoundError
import os
from domain.usecases.grader_analyzer_usecase import GraderAnalyzerUsecase
from infrastructure.messaging.nats_subscribe import NatsSubscriber
from infrastructure.logger.logger import StandardLogger
from infrastructure.mongo.mongo import MongoDB
from infrastructure.mongo.repositories.exam_repository import ExamRepository
from infrastructure.mongo.repositories.summary_qualification_respository import SummaryQualificationRepository
from infrastructure.mongo.repositories.template_repository import TemplateRepository


# # Ejecutar el programa
# if __name__ == "__main__":
#     mongo_client = MongoDB()
#     logger = StandardLogger()
#     exam_repo = ExamRepository(mongo=mongo_client)
#     template_repo = TemplateRepository(mongo=mongo_client)
#     summary_repo = SummaryQualificationRepository(mongo=mongo_client)
#     usecase = GraderAnalyzerUsecase(exam_repo=exam_repo,
#                                     temp_repo=template_repo,
#                                     summary_repo=summary_repo,
#                                     logger=logger)

#     usecase.analyze("681402fedfa5d350c38ac963")
STREAM_NAME = "cv-grader-analyzer"
EVENT_PROCESS_EXAM = "process.exam"
logger = StandardLogger()


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
        logger.info(info)
        existing_subjects = set(info.config.subjects)
        if set(desired["subjects"]) != existing_subjects:
            # Actualizamos sólo la parte que cambió
            cfg = info.config
            cfg.subjects = desired["subjects"]
            await js.update_stream(cfg)
            logger.info(f"🔄 Stream '{STREAM_NAME}' updated.")
        else:
            logger.info(f"✅ Stream '{STREAM_NAME}' exists")
    except NotFoundError:
        # No existe → lo creamos
        await js.add_stream(**desired)
        logger.info(f"✅ Stream '{STREAM_NAME}' created.")

async def main():
    nc = NATS()
    host = os.getenv("NATS_URL","")
    if host == "":
        raise ValueError("NATS_HOST is not set")
    await nc.connect(host)
    js = nc.jetstream()
    await ensure_stream(js)
    # Crear stream si no existe
    await js.add_stream(name=STREAM_NAME, subjects=[EVENT_PROCESS_EXAM])

    mongo_client = MongoDB()
    exam_repo = ExamRepository(mongo=mongo_client)
    template_repo = TemplateRepository(mongo=mongo_client)
    summary_repo = SummaryQualificationRepository(mongo=mongo_client)
    usecase = GraderAnalyzerUsecase(exam_repo=exam_repo,
                                    temp_repo=template_repo,
                                    summary_repo=summary_repo,
                                    logger=logger)
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
