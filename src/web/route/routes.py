from datetime import datetime, timezone
from fastapi import APIRouter, Form, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from src.web.model.model import CheckResponseSchema
from typing import List

from pathlib import Path

router = APIRouter()

def init_routes(container):
    #upload_checks = container.upload_checks()
    check_service = container.check_service()
    repository = container.repository()
    #load_check_service = container.load_check_service()
    @router.get('/')
    def init():
        return {
            "status": "success",
            "message": "Добро пожаловать на сайт обработки документов"
        }
    @router.post('/api/checks')
    async def load_docks(
            program: str = Form(...),
            files: List[UploadFile] = File(...)
    ):
        if not files:
            return JSONResponse(status_code=400, content={"error": "не загружены файлы"})

        incoming_files = []
        for file in files:
            # позже сюда добавятся и проверки содержимого
            # await file.read()
            path = Path(file.filename or "unnamed")

            incoming_files.append({
                "name": file.filename or "unnamed",
                "size_bytes": file.size or 0,
                "stem": path.stem,
                "ext": path.suffix
            })

        check_result = check_service.checking(incoming_files, program)
        packet_id = await repository.save_data(
            program_type=program,
            status=check_result["status"],
            status_label=check_result["status_label"],
            reason=check_result["reason"],
            issues=check_result["issues"],
            extracted=check_result["extracted"],
            documents_data=check_result["documents"]
        )
        result_response = CheckResponseSchema(
            check_id=str(packet_id),
            status=check_result["status"],
            status_label=check_result["status_label"],
            reason=check_result["reason"],
            issues=check_result["issues"],
            documents=check_result["documents"],
            extracted=check_result["extracted"],
            checked_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        )
        for file in files:
            await file.close()

        if check_result["status"] == "reject":
            return JSONResponse(status_code=400, content=result_response.model_dump())
        return result_response

    @router.get('/api/checks')
    async def get_checks():
        result = await repository.get_full_checks()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при получению данных из базы"
            )
        return [
            {
                "id": str(row.id),
                "date": row.created_at.isoformat() + "Z" if row.created_at else None,
                "program": row.program_type,
                "status": row.status,
                "documents_count": row.documents_count
            }
            for row in result
        ]

    @router.get('/api/checks/{check_id}')
    async def get_check_result(check_id: int):
        result = await repository.get_check_with_id(check_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Проверка с ID {check_id} не найдена"
            )
        check_data, documents = result
        return {
            "check_id": str(check_data.id),
            "status": check_data.status,
            "status_label": check_data.status_label,
            "reason": check_data.reason,
            "issues": check_data.issues or [],  # Защита от None в JSON-поле
            "documents": [
                {
                    "name": doc.docs_name,
                    "detected_type": doc.detected_type,
                    "size_kb": doc.size_kb
                }
                for doc in documents
            ],
            "extracted": check_data.extracted or {},  # Защита от None
            "checked_at": check_data.created_at.isoformat() + "Z" if check_data.created_at else None
        }

    return router


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