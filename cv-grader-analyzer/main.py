from domain.usecases.grader_analyzer_usecase import GraderAnalyzerUsecase
from infrastructure.logger.logger import StandardLogger
from infrastructure.mongo.mongo import MongoDB
from infrastructure.mongo.repositories.exam_repository import ExamRepository
from infrastructure.mongo.repositories.summary_qualification_respository import SummaryQualificationRepository
from infrastructure.mongo.repositories.template_repository import TemplateRepository


# Ejecutar el programa
if __name__ == "__main__":
    mongo_client = MongoDB()
    logger = StandardLogger()
    exam_repo = ExamRepository(mongo=mongo_client)
    template_repo = TemplateRepository(mongo=mongo_client)
    summary_repo = SummaryQualificationRepository(mongo=mongo_client)
    usecase = GraderAnalyzerUsecase(exam_repo=exam_repo,
                                    temp_repo=template_repo,
                                    summary_repo=summary_repo,
                                    logger=logger)

    usecase.analyze("681392dc6f4cd587865ae0e1")
