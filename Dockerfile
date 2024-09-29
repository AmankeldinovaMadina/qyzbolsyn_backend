# Start with an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN  -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for FastAPI
ENV PYTHONUNBUFFERED=1

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
