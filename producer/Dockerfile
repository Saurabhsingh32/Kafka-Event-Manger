# Use the official Python 3.13.3 slim image as the base for Flask
FROM python:3.13.3-slim AS flask-app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /producer/

# Install dependencies
COPY producer-requirements.txt .
RUN pip3 install -r producer-requirements.txt --no-cache-dir

# Copy project
COPY . .

# Expose the port the app runs on
EXPOSE 5001

CMD ["python", "producer.py"]


