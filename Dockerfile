# Use the official Python 3.11 slim image as the base image
FROM python:3.11-slim

# Install PortAudio and other system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE $PORT

# Run the application
CMD ["python", "app.py"]