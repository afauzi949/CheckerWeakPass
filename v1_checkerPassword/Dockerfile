# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Step 2: Update and upgrade the system packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN pip install --upgrade pip

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose port 5000 for Flask application
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
