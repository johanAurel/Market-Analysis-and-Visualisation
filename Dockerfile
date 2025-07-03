FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    libffi-dev \
    musl-dev \
    build-base \
    py3-pip \
    python3-dev \
    openssl-dev

# Copy and install dependencies
COPY /code/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY /code /app/

# Run the app
CMD [ "python3", "controller.py" ]

