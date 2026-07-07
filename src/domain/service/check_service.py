from typing import Dict, List
from src.domain.model.model import ProgramType
class CheckService:
    def __init__(self):
        self.max_byte_size = 20*1024*1024

    def checking(self, incoming_files: List[Dict], program_name: str) -> Dict:
        issues = []
        documents_report = []
        detected_types = set()

        if not program_name:
            issues.append({"level": "error", "message": "Не указан тип программы"})
            program_name = ""
        elif program_name.lower() not in [e.value for e in ProgramType]:
            issues.append({"level": "error", "message": f"Неверный тип программы: {program_name}"})

        for file in incoming_files:
            full_name = file["name"]
            size_bytes = file["size_bytes"]
            name = file["stem"]
            ext = file["ext"]
            size_kb = max(1, size_bytes // 1024)

            if size_bytes > self.max_byte_size:
                issues.append({"level": "error", "message": f"Файл {full_name} имеет размер ({size_kb} КБ)"})
            if size_bytes == 0:
                issues.append({"level": "error", "message": f"Файл {full_name} пустой"})

            if ext.upper() not in [".PDF", ".DOCX", ".JPG", ".PNG"]:
                issues.append({"level": "warning", "message": f"Недопустимый формат файла: {full_name}"})

            detected_type = None
            if "договор" in name.lower():
                detected_type = "contract"
                detected_types.add("договор")
            elif "спецификация" in name.lower():
                detected_type = "specification"
                detected_types.add("спецификация")
            elif "счёт" in name.lower() or "счет" in name.lower():
                detected_type = "invoice"
                detected_types.add("счёт")
            elif "акт" in name.lower():
                detected_type = "act"
                detected_types.add("акт")
            elif "УПД" in name.upper():
                detected_type = "upd"
                detected_types.add("УПД")
            else:
                issues.append({"level": "warning", "message": f"Не удалось определить тип документа: {full_name}"})

            documents_report.append({
                "name": full_name,
                "detected_type": detected_type,
                "size_kb": size_kb
            })

        has_pack_error = False
        reason_msg = None

        if program_name == "federal":
            required_docs = {"договор", "спецификация", "счёт"}
            if not (required_docs <= detected_types and ("акт" in detected_types or "УПД" in detected_types)):
                has_pack_error = True
                reason_msg = "Для программы federal нужны следующие документы: договор, спецификация, счёт, акт/УПД)."
                issues.append({"level": "error", "message": "Загружен неполный комплект документов"})
        elif program_name == "regional":
            required_docs = {"договор", "счёт"}
            if not (required_docs <= detected_types and ("акт" in detected_types or "УПД" in detected_types)):
                has_pack_error = True
                reason_msg = "Отсутствуют обязательные документы для программы regional (требуются: договор, счёт, акт/УПД)."
                issues.append({"level": "error", "message": "Загружен неполный комплект документов"})

        has_any_error = any(issue["level"] == "error" for issue in issues) or has_pack_error
        if has_any_error:
            status = "reject"
            status_label = "Нельзя заявлять в банк"
        else:
            status = "approved"
            status_label = "Успешно проверено"
            reason_msg = "Все проверки пройдены"

        # здесь еще должны быть блоки программ, парсящих файлы,
        # а до этого эти файлы еще надо скачать,
        # сейчас стоит просто заглушка

        contractor = "ООО «ТехАгро»"
        amount = "1 250 000 ₽"
        date = "01.03.2025"
        subject = "Поставка минеральных удобрений"

        extracted_data = {"contractor": contractor if status == "approved" else None,
                          "amount": amount if status == "approved" else None,
                          "date": date if status == "approved" else None,
                          "subject": subject if status == "approved" else None

        }

        return {
            "status": status,
            "status_label": status_label,
            "reason": reason_msg,
            "issues": issues,
            "documents": documents_report,
            "extracted": extracted_data
        }
