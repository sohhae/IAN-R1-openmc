# Dockerfile for IAN-R1-openmc
FROM python:3.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    gfortran \
    cmake \
    git \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir openmc numpy matplotlib

# Set the working directory inside the container
WORKDIR /app

# Default command (you can override it when running)
CMD ["python", "/app/Code/main_model.py"]
