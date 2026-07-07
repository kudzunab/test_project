from sqlalchemy.exc import SQLAlchemyError
from src.datasource.model.model import RequestStatus, DocumentsList
from sqlalchemy import select, func

class Repository:
    def __init__(self, session_factory):
        self.session_factory=session_factory

    async def save_data(
            self,
            program_type: str,
            status: str,
            status_label: str,
            reason: str,
            issues: list,
            extracted: dict,
            documents_data: list[dict]  # Переименовали для понятности, так как это список словарей, а не просто строк
    ):
        try:
            async with self.session_factory() as session:
                async with session.begin():

                    db_request_status = RequestStatus(
                        program_type=program_type,
                        status=status,
                        status_label=status_label,
                        reason=reason,
                        issues=issues,
                        extracted=extracted
                    )
                    session.add(db_request_status)

                    await session.flush()
                    returned_id = db_request_status.id

                    db_documents = [
                        DocumentsList(
                            packet_id=returned_id,
                            docs_name=doc["name"],
                            detected_type=doc["detected_type"],
                            size_kb=doc["size_kb"]
                        )
                        for doc in documents_data
                    ]

                    session.add_all(db_documents)

            return returned_id
        except SQLAlchemyError as exc:
            print(f"Ошибка сохранения в базу данных: {exc}")
            return None

    async def get_full_checks(self):
        try:
            async with self.session_factory() as session:
                async with session.begin():
                    query = select(RequestStatus.id,
                                   RequestStatus.created_at,
                                   RequestStatus.program_type,
                                   RequestStatus.status,
                                   func.count(DocumentsList.docs_id).label("documents_count")
                                   )\
                        .join(DocumentsList, DocumentsList.packet_id == RequestStatus.id)\
                        .group_by(RequestStatus.id)\
                        .order_by(RequestStatus.created_at.desc())
                    result = await session.execute(query)
            return result.all()

        except SQLAlchemyError as exc:
            print(f"Ошибка сохранения в базу данных: {exc}")
            return None

    async def get_check_with_id(self, check_id):
        try:
            async with (self.session_factory() as session):
                async with session.begin():
                    status_query = select(RequestStatus).where(RequestStatus.id == int(check_id))
                    status_result = await session.execute(status_query)
                    check_data = status_result.scalar_one_or_none()
                    if not check_data:
                        return None
                    docs_query = select(DocumentsList).where(DocumentsList.packet_id == int(check_id))
                    docs_result = await session.execute(docs_query)
                    documents = docs_result.scalars().all()
            return check_data, documents

        except SQLAlchemyError as exc:
            print(f"Ошибка сохранения в базу данных: {exc}")
            return None
