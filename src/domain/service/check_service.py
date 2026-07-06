from typing import Dict
class CheckService:
    def __init__(self):
        self.max_byte_size = 20*1024*1024

    def checking(self, param_dict: Dict, program_name: str):
        error_list = []
        warning_list = []
        documents = []
        if not program_name:
            error_list.append("не указан тип программы")
            return False

        for key in param_dict:
            for ind, val in enumerate(param_dict[key]["size"]):
                if val == 0:
                    error_list.append(f"{key}_{ind} не имеет размера")

                if param_dict[key]["size"][ind] > self.max_byte_size:
                    error_list.append(f"{key}_{ind} имеет слишком большорй размер")

                if not param_dict[key]["name"][ind]:
                    error_list.append(f"{key}_{ind} не имеет атрибута имени")

                if not param_dict[key]["ext"][ind]:
                    error_list.append(f"{key}_{ind} не имеет расширения")

                if param_dict[key]["ext"][ind].upper() not in [".PDF", ".DOCX", ".JPG", ".PNG"]:
                    error_list.append(f"{key}_{ind} имеет непрапвльное расширение")

                if "договор" in param_dict[key]["name"][ind].lower():
                    documents.append("договор")
                elif "спецификация" in param_dict[key]["name"][ind].lower():
                    documents.append("спецификация")
                elif "счёт" in param_dict[key]["name"][ind].lower():
                    documents.append("счёт")
                elif "акт" in param_dict[key]["name"][ind].lower():
                    documents.append("акт")
                elif "УПД" in param_dict[key]["name"][ind].upper():
                    documents.append("УПД")
                else:
                    warning_list.append(f"Нераспознанное имя документа {key}_{ind}")

        if program_name == "federal" and (({"договор", "спецификация", "счёт", "акт"} <= set(documents)  or
                {"договор", "спецификация", "счёт", "УПД"} <= set(documents))):
            if not error_list:
                return True, warning_list, []
            else:
                return False, warning_list, error_list

        if program_name == "regional" and ({"договор", "счёт", "акт"} <= set(documents)
                                           or {"договор", "счёт", "УПД"} <= set(documents)):
            if not error_list:
                return True, warning_list, []
            else:
                return False, warning_list, error_list

        error_list.append("загружен неполный комплдект документов")
        return False, warning_list, error_list