from src.application.interfaces.services import IFileLoadStorage
from abc import ABC, abstractmethod
from typing import List
from fastapi import UploadFile
import asyncio
from fastapi.responses import JSONResponse
import uuid
import os
import aiofiles
from pathlib import Path

class LoadService(IFileLoadStorage):
    def __init__(self):
        self.size = 1024 * 64

    async def save_files(self, files: List[UploadFile], unique_uuid: str):
        saved_files = []
        for file in files:
            full_name = file.filename
            file_name = Path(full_name).stem
            file_ext = Path(full_name).suffix
            file_uuid = str(uuid.uuid4())
            uniq_name = f"{file_uuid}_{file_name}"
            file_size = file.size
            path_file = f"{unique_uuid}_{uniq_name}{file_ext}"
            success = False

        return saved_files


"""
    async def save_files(self, files: List[UploadFile], unique_uuid: str):
        saved_files = []
        for file in files:
            full_name = file.filename
            file_name = Path(full_name).stem
            file_ext = Path(full_name).suffix
            file_uuid = str(uuid.uuid4())
            uniq_name = f"{file_uuid}_{file_name}"
            path_file = f"{unique_uuid}_{uniq_name}{file_ext}"
            success = False
            try:
                async with aiofiles.open(path_file, "wb") as my_file:
                    while True:
                        try:
                            part = await asyncio.wait_for(file.read(self.size), timeout=20)
                        except asyncio.TimeoutError:
                            print(f"Соединение зависло при загрузке {full_name}")
                            break
                        if not part:
                            success = True
                            saved_files.append(path_file)
                            break
                        await my_file.write(part)
            except (IOError, Exception) as e:
                print(f"Сетевой обрыв при загрузке файла {full_name}: {e}")
            finally:
                await file.close()
                if not success:
                    if os.path.exists(path_file):
                        os.remove(path_file)
                        print(f"Удален недокачанный файл: {path_file}")

                    for path in saved_files:
                        os.remove(path)
                        print(f"Удален недокачанный файл {path}")
                    raise IOError(f"Загрузка пачки прервана на файле: {full_name}")

        return saved_files
"""