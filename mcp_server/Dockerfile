FROM python:3.12-slim

RUN apt update && apt install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data (Recipes_en.csv)
COPY . /app

EXPOSE 9000
CMD ["python", "mcp_server.py"]