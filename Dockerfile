FROM python:3.11.7-slim-bullseye 

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    libmagic-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install poetry --no-cache-dir 
RUN poetry self add poetry-plugin-dotenv
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN poetry install --only main

COPY . /app
EXPOSE 8502

RUN mkdir -p /app/data

CMD ["poetry", "run", "streamlit", "run", "app_home.py"]
