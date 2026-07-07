#!/bin/bash

echo "Ожидание запуска PostgreSQL"
sleep 5

echo "Применяем миграцию Alembic"
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "Ошибка: Миграции Alembic не смогли примениться!"
    exit 1
fi

echo "Запуск тестов Pytest"
python -m pytest -v
if [ $? -ne 0 ]; then
    echo "Ошибка: Тесты провалились! Запуск сервера отменен."
    exit 1
fi

echo "Тесты успешно пройдены!"

echo "Запуск сервера FastAPI"
cp .env_for_use .env
python src/main.py