# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements
RUN pip install --no-cache-dir flask picamera2 opencv-python

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run stream.py when the container launches
CMD ["python", "stream_with_auth.py"]
