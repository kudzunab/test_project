from dependency_injector import containers, providers
#from src.application.service.load_service import LoadService
#from src.application.use_cases.upload_check import UploadChecksUseCase
from src.datasource.service.repository import Repository
from src.domain.service.check_service import CheckService
from src.datasource.service.connection import init_my_db
class Container(containers.DeclarativeContainer):
    #load_service = providers.Singleton(LoadService)
    check_service = providers.Singleton(CheckService)
    session_factory = providers.Object(init_my_db())
    repository = providers.Singleton(
        Repository,
        session_factory=session_factory
    )
    #upload_checks = providers.Factory(
    #    UploadChecksUseCase,
    #    load_service=load_service,
    #    check_service=check_service
    #)