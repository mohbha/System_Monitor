# 1. Base Image
FROM python:3.9-slim

# 2. Working directory inside container
WORKDIR /app

# 3. Copy dependency list
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . .

# 6. Expose API port
EXPOSE 8000

# 7. Run the service
CMD ["python", "main.py"]