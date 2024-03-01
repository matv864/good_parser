# Start your image with a node base image
FROM pypy:3.10-7.3.15-bullseye

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app


# Copy the app package and package-lock.json file11
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы из локальной директории в рабочую директорию внутри контейнера
COPY . /app



CMD ["python3", "main.py"]