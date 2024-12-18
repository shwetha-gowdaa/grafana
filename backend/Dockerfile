FROM python:3.9-slim

# Install PostgreSQL dependencies and build tools
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Start the Flask app with the appropriate host and port
CMD ["python", "app.py", "--host=0.0.0.0"]
