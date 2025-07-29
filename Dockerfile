FROM python:slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    python3-dev \
    libstdc++-12-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN pip install --upgrade transformers

COPY ./src /app/

RUN chmod +x /app/script.sh

ENTRYPOINT ["/app/script.sh"]