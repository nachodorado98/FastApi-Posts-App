FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "run:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
