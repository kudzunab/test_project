from dependency_injector import containers, providers
#from src.application.service.load_service import LoadService
#from src.application.use_cases.upload_check import UploadChecksUseCase
from src.domain.service.check_service import CheckService
class Container(containers.DeclarativeContainer):
    #load_service = providers.Singleton(LoadService)
    check_service = providers.Singleton(CheckService)
    #upload_checks = providers.Factory(
    #    UploadChecksUseCase,
    #    load_service=load_service,
    #    check_service=check_service
    #)