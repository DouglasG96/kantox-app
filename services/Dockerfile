# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Command to run the application
CMD ["python", "auxiliary_service.py"]
EXPOSE 6000