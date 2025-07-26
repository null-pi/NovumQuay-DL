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

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install --upgrade transformers

COPY script.sh .
RUN chmod +x script.sh

COPY /src .

EXPOSE 8000

ENTRYPOINT ["./script.sh"]