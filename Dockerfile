# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install Flask
RUN pip install flask

# Copy your application code
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask app
# CMD ["sh", "-c", "python main.py; tail -f /dev/null"]


