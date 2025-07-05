FROM python:2.7-alpine

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    gfortran \
    libffi-dev \
    freetype-dev \
    libpng-dev \
    pkgconfig \
    openblas-dev \
    && pip install --upgrade pip setuptools wheel

# Copy requirements.txt
COPY requirements.txt .

# Install compatible older versions of packages for Python 2
RUN pip install \
    "pandas<1.0" \
    "numpy<1.17" \
    matplotlib==2.2.5 \
    questionary==1.10.0 \
    requests

# Remove build dependencies to keep image small
RUN apk del .build-deps
