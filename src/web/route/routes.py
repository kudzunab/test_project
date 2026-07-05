from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from src.web.model.model import ProgramType
from src.di.container import Container
import asyncio
import uuid
import os
import aiofiles
from pathlib import Path
app = FastAPI()
def init_routes(app, container):
    upload_checks = container.upload_checks()
    @app.route('api/checks', methods=['POST'])
    async def load_docks():

        program: ProgramType = Form(...)
        if program not in ['federal', 'regional']:
            return JSONResponse(status_code=400, content={"error": "неверная программа"})
        files: List[UploadFile] = File(...)
        unique_uuid = str(uuid.uuid4())
        if not files:
            return JSONResponse(status_code=400, content={"error": "не загружены файлы"})
        saved_files = []
        for file in files:
            full_name = file.filename
            file_name = Path(full_name).stem
            file_ext = Path(full_name).suffix
            file_uuid = str(uuid.uuid4())
            uniq_name = f"{file_uuid}_{file_name}"
            path_file = f"{unique_uuid}_{uniq_name}{file_ext}"
            success = False
            size = 1024*64
            try:
                async with aiofiles.open(path_file, "wb") as my_file:
                    while True:
                        try:
                            part = await asyncio.wait_for(file.read(size), timeout=20)
                        except asyncio.TimeoutError:
                            print(f"Соединение зависло при загрузке {full_name}")
                            break
                        if not part:
                            success = True
                            saved_files.append(path_file)
                            break
                        await my_file.write(part)
            except (IOError, Exception) as e:
                print (f"Сетевой обрыв при загрузке файла {full_name}: {e}")
            finally:
                await file.close()
                if not success:
                    if os.path.exists(path_file):
                        os.remove(path_file)
                        print(f"Удален недокачанный файл: {path_file}")

                    for path in saved_files:
                        os.remove(path)
                        print(f"Удален недокачанный файл {path_file}")
                    return JSONResponse(status_code=408, content={"error": f"Загрузка прервана: {full_name}"})

        return {"status": "success", "data": []}
    @app.route('api/checks', methods=['GET'])
    async def load_docks():
        return None, 201
    @app.route('api/checks/{id}', methods=['GET'])
    def load_docks(id):
        files: List
        if not get_check_result(id):
           return  "не верный id заявки", 400
        return get_check_result(id), 201