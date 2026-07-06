"""

import uuid
from typing import List
from fastapi import UploadFile
from src.application.interfaces.services import IFileLoadStorage


class UploadChecksUseCase:
    def __init__(self, load_service: IFileLoadStorage):
        self.load_service = load_service  # Внедряем интерфейс

    async def execute(self, files: List[UploadFile]) -> List[str]:

        unique_uuid = str(uuid.uuid4())
        saved_paths = await self.load_service.save_files(files, unique_uuid)

        return saved_paths
    async def cheking(self, mass_names: List[str], type_program: str):
        result = False
        number = 0
        if type_program not in ["federal", "regional"]:
            print("не верный тип программы")
            return result

        for name in mass_names:
            if
            number += 1

"""