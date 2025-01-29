# Use a lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies (if required)
RUN pip install --no-cache-dir -r requirements.txt || echo "No dependencies"

# Run the blockchain simulation
CMD ["python", "main.py"]
