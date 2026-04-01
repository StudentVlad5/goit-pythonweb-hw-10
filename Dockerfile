FROM python:3.13-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо інструменти для збірки
RUN pip install --no-cache-dir poetry

# Копіюємо файл конфігурації
COPY pyproject.toml /app/

# Налаштовуємо Poetry: не створювати віртуальне оточення 
# та встановлюємо залежності безпосередньо (це працює і без плагіна export)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-cache

# Копіюємо всі файли проекту в /app
COPY . /app/

# Запуск. Оскільки main.py в корені
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]