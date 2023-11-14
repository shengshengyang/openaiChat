# Use an official Python runtime as a parent image
FROM python:3.7-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run queryConnectOpenAiApi.py when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "controller:app"]

