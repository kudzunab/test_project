import pytest
from src.domain.service.check_service import CheckService

@pytest.fixture
def check_service():
    return CheckService()

"""
    1 тест: Сначала проверяем работу на корректных данных
"""
def test_federal_program_success(check_service):
    incoming_files = [
        {"name": "договор_поставки_№12.pdf", "size_bytes": 1024 * 100, "stem": "договор_поставки_№12", "ext": ".pdf"},
        {"name": "спецификация_финал.docx", "size_bytes": 1024 * 50, "stem": "спецификация_финал", "ext": ".docx"},
        {"name": "счёт_на_оплату.jpg", "size_bytes": 1024 * 200, "stem": "счёт_на_оплату", "ext": ".jpg"},
        {"name": "акт_приемки.png", "size_bytes": 1024 * 150, "stem": "акт_приемки", "ext": ".png"},
    ]

    result = check_service.checking(incoming_files, "federal")

    assert result["status"] == "approved"
    assert result["status_label"] == "Успешно проверено"
    assert result["reason"] == "Все проверки пройдены"
    assert len(result["issues"]) == 0
    assert len(result["documents"]) == 4

"""
    2 тест: Проверяем другую правильную версию документов
"""
def test_federal_program_with_upd_success(check_service):
    incoming_files = [
        {"name": "договор_основной.pdf", "size_bytes": 5000, "stem": "договор_основной", "ext": ".pdf"},
        {"name": "спецификация_v2.docx", "size_bytes": 12000, "stem": "спецификация_v2", "ext": ".docx"},
        {"name": "счет_фактура.jpg", "size_bytes": 45000, "stem": "счет_фактура", "ext": ".jpg"},
        {"name": "УПД_от_марта.pdf", "size_bytes": 98000, "stem": "УПД_от_марта", "ext": ".pdf"},  # УПД заменяет Акт
    ]

    result = check_service.checking(incoming_files, "federal")

    assert result["status"] == "approved"

    upd_doc = next(d for d in result["documents"] if "УПД" in d["name"])
    assert upd_doc["detected_type"] == "upd"

"""
    3 тест: Проверяем неполный комплект документов
"""
def test_regional_program_missing_invoice(check_service):
    incoming_files = [
        {"name": "договор_аренды.pdf", "size_bytes": 5000, "stem": "договор_аренды", "ext": ".pdf"},
        {"name": "акт_сдачи.pdf", "size_bytes": 3000, "stem": "акт_сдачи", "ext": ".pdf"},
        # По ТЗ для regional обязательны: договор, счёт, акт. Счёта нет!
    ]

    result = check_service.checking(incoming_files, "regional")

    assert result["status"] == "reject"
    assert result["status_label"] == "Нельзя заявлять в банк"
    assert any("Загружен неполный комплект документов" in issue["message"] for issue in result["issues"])

"""
    4 тест: Неверное программы
"""
def test_invalid_program_name(check_service):
    incoming_files = [
        {"name": "договор.pdf", "size_bytes": 5000, "stem": "договор", "ext": ".pdf"}
    ]

    result = check_service.checking(incoming_files, "international")

    assert result["status"] == "reject"
    assert any("Неверный тип программы" in issue["message"] for issue in result["issues"])

"""
    5 тест: Неверное программы
"""
def test_file_exceeds_max_size(check_service):
    too_large_size = 25 * 1024 * 1024  # 25 МБ в байтах
    incoming_files = [
        {"name": "договор.pdf", "size_bytes": 5000, "stem": "договор", "ext": ".pdf"},
        {"name": "счет.pdf", "size_bytes": 4000, "stem": "счет", "ext": ".pdf"},
        {"name": "акт_скан_высокое_разрешение.pdf", "size_bytes": too_large_size, "stem": "акт_скан_высокое_разрешение",
         "ext": ".pdf"},
    ]

    result = check_service.checking(incoming_files, "regional")

    assert result["status"] == "reject"
    assert any("имеет размер" in issue["message"] for issue in result["issues"])

"""
    6 тест: Нераспознанные имена файлов
"""
def test_warnings_behavior(check_service):
    incoming_files = [
        {"name": "договор.pdf", "size_bytes": 5000, "stem": "договор", "ext": ".pdf"},
        {"name": "счет.pdf", "size_bytes": 4000, "stem": "счет", "ext": ".pdf"},
        {"name": "акт.pdf", "size_bytes": 3000, "stem": "акт", "ext": ".pdf"},
        {"name": "архив.zip", "size_bytes": 2000, "stem": "архив", "ext": ".zip"},  # Неверный формат (.zip)
        {"name": "неизвестный_файл.pdf", "size_bytes": 1000, "stem": "неизвестный_файл", "ext": ".pdf"},
    ]

    result = check_service.checking(incoming_files, "regional")

    assert result["status"] == "approved"

    warnings = [issue for issue in result["issues"] if issue["level"] == "warning"]
    assert len(warnings) == 3