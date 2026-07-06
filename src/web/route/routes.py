from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
#from src.domain.model.model import ProgramType

from pathlib import Path
app = FastAPI()
def init_routes(app, container):
    #upload_checks = container.upload_checks()
    check_service = container.check_service()
    #load_check_service = container.load_check_service()
    @app.post('/api/checks')
    async def load_docks(
            program: str = Form(...),
            files: List[UploadFile] = File(...)
    ):
        error_list = []
        #unique_uuid = str(uuid.uuid4())

        if not files:
            return JSONResponse(status_code=400, content={"error": "не загружены файлы"})

        file_dict = {}

        for file in files:
            full_name = file.filename
            if not full_name:
                error_list.append("файл не загружен или не имеет имени")
                continue

            name, ext, size = "", "", 0
            if Path(full_name).stem:
                name = Path(full_name).stem

            if Path(full_name).suffix:
                ext = Path(full_name).suffix

            if file.size:
                size = file.size

            if full_name not in file_dict:
                file_dict[full_name] = {"name": [name], "ext": [ext], "size": [size]}
            else:
                file_dict[full_name]["name"].append(name)
                file_dict[full_name]["ext"].append(ext)
                file_dict[full_name]["size"].append(size)
                error_list.append(f"Файл {full_name} с таким именем уже был загружен")

            await file.close()
        is_ok, warning_list, error_list_0 = check_service.checking(file_dict, program)
        error_list.extend(error_list_0)
        if is_ok:
            for war in warning_list:
                print(war)

            return JSONResponse(status_code=200, content={"status": "approved", "warnings": warning_list})

        return JSONResponse(status_code=400, content={"status": "rejected", "warnings": warning_list,
                                                      "errors": error_list})

            #file_uuid = str(uuid.uuid4())
            #uniq_name = f"{file_uuid}_{file_name}"
            #path_file = f"{unique_uuid}_{uniq_name}{file_ext}"
"""
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
"""