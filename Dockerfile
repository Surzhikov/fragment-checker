# Используйте официальный образ Python как базовый
FROM python:3.9-slim

# Установите рабочий каталог в контейнере
WORKDIR /usr/src/app

# Копируйте файлы скрипта в рабочий каталог
COPY check.py .

# Установите необходимые библиотеки
RUN pip install --no-cache-dir requests beautifulsoup4

# Укажите команду для запуска Python скрипта
CMD ["python", "./check.py"]
