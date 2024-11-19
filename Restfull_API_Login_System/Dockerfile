

# Use an official Python runtime as a parent image
FROM python:3.12.4

# Set the working directory in the container
WORKDIR /Restfull_API_Login_System

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY . .

# Expose the port your FastAPI app runs on
EXPOSE 9000

# Define the command to run your app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

