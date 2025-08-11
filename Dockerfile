FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TEMPORAL_HOST=localhost:7233

EXPOSE 8000

ENTRYPOINT ["python", "app.py"]
CMD ["--help"]