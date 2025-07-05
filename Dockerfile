FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3"]
