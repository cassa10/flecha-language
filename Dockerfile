FROM python:3.11.6-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

RUN python3 -m pytest

CMD ["python3", "./src/main.py", "-h"]