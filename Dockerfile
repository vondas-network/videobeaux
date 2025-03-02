# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the Python script executable
RUN chmod +x videobeaux.py

# Define the command to run the CLI tool
ENTRYPOINT ["python3", "videobeaux.py"]
