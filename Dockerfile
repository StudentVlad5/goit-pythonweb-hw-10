# 1. Використовуємо офіційний образ Python
FROM python:3.13-slim

# 2. Встановлюємо робочу директорію
WORKDIR /app

# 3. Встановлюємо змінні оточення, щоб Python не створював .pyc файли та виводив логи відразу
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Встановлюємо Poetry
RUN pip install --no-cache-dir poetry

# 5. Копіюємо лише файли конфігурації залежностей
# Це дозволяє Docker кешувати шар із залежностями
COPY pyproject.toml poetry.lock* /app/

# 6. Налаштовуємо Poetry: не створювати віртуальне оточення (в контейнері воно не потрібне)
# Та встановлюємо залежності
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 7. Копіюємо решту коду проєкту
COPY . /app/

# 8. Команда для запуску (FastAPI + Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]