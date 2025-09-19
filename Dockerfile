FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for OpenMC
RUN apt-get update && apt-get install -y \
    gfortran \
    libopenmpi-dev \
    openmpi \
    cmake \
    git \
    libhdf5-dev \
    libpng-dev

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set the default command to run the main model
CMD ["python", "Code/main_model.py"]

