# Example for backend Dockerfile
# Use Python 3.10 slim as the base image
FROM python:3.10-slim

# Set the working directory to /app in the container
WORKDIR /app

# Copy the backend code into the container's /app directory
COPY backend/ /app/
COPY requirements.txt /app/requirements.txt


# Copy the .env file for environment variables
COPY .env.example /app/.env

# Install dependencies
RUN pip3 install -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]