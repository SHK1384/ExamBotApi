# Use an official Python runtime as a parent image
FROM hub.hamdocker.ir/library/python:3.13

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev
# Add PostgreSQL dependencies if you're using PostgreSQL

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Run Django commands inside Docker
CMD ["gunicorn", "ExamBotApi.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "9", "--timeout", "120"]