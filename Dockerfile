# Using the base image from your course PDF
FROM python:3.11

# Set environment variables for better logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Port for Django
EXPOSE 8000

# Command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]