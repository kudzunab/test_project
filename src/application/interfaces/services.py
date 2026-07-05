from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile
class IFileLoadStorage(ABC):
    @abstractmethod
    async def save_files(self, files: List[UploadFile], unique_uuid: str) -> List[str]:
        """
        Принимает список файлов, сохраняет их и
        возвращает список ссылок или путей для базы данных.
        """
        pass