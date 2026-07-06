import uuid
from sqlalchemy.exc import SQLAlchemyError
from src.datasource.model.model import RequestStatus, DocumentsList

class Repository:
    def __init__(self, session_factory):
        self.session_factory=session_factory

    def save_data(self, list_of_names: list[str], program_type: str,status: str = ""):
        try:
            with self.session_factory() as session:
                with session.begin():
                    db_request_status = RequestStatus(program_type = program_type, status = status)
                    session.add(db_request_status)

            return True
        except SQLAlchemyError as exc:
            print(f"Ошибка сохранения в базу данных: {exc}")
            return False