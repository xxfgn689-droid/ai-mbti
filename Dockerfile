FROM python:3.11-slim

WORKDIR /app

COPY requirements_zeabur.txt .
RUN pip install --no-cache-dir -r requirements_zeabur.txt

COPY . .

EXPOSE 3000

CMD ["python", "app.py"]