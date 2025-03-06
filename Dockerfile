FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директории для логов
RUN mkdir -p logs

# Экспорт порта
EXPOSE 8085

# Запуск через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8085", "--workers", "4", "run:app"]