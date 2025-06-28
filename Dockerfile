FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY script.sh .
RUN chmod +x script.sh

COPY /src .

EXPOSE 8000

ENTRYPOINT ["./script.sh"]