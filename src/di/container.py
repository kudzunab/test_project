from dependency_injector import containers, providers
from src.application.service.load_service import LoadService
from src.application.use_cases.upload_check import UploadChecksUseCase
class Container(containers.DeclarativeContainer):
    load_service = providers.Singleton(LoadService)
    upload_checks = providers.Factory(
        UploadChecksUseCase,
        load_service=load_service
    )