# в корне проекта: alembic init -t async alembic
# psql -U admin -d postgres
#environment:
#  POSTGRES_USER: postgres
#  POSTGRES_PASSWORD: your_password
#  POSTGRES_DB: звание базы банных
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
# зупуск тестов  python -m pytest -v

import sys
from pathlib import Path
from src.application.module.module import main

sys.path.append(str(Path(__file__).parent.parent))
if __name__ == "__main__":
    main()