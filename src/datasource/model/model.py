from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime, func, BigInteger
from datetime import datetime

class Base(DeclarativeBase):
    pass

#def get_new_uuid():
#    return str(uuid.uuid4())

class RequestStatus(Base):
    __tablename__ = "request_status"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    program_type: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="check_in_progress")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

class DocumentsList(Base):
    __tablename__ = "documents_info"
    docs_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    packet_uuid: Mapped[int|None] = mapped_column(BigInteger, ForeignKey('request_status.id', name="fk_paket_id",
                                                                    ondelete="SET NULL"), nullable=True)
    list_of_docs_uuid: Mapped[str] = mapped_column(String)