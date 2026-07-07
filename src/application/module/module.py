from fastapi import FastAPI
import uvicorn
from src.di.container import Container
from src.web.route.routes import init_routes

app = FastAPI(
    title="Сервис проверки документов",
    description="REST API для валидации комплектности пакетов документов",
    version="1.0.0")

container = Container()
app.container = container
checks_router = init_routes(container)
app.include_router(checks_router)


def main():
    uvicorn.run("src.application.module.module:app", host="0.0.0.0", port=8000, reload=True)
