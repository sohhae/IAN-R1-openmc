FROM python:3.11-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    gfortran \
    cmake \
    git \
    libopenmpi-dev \
    openmpi-bin \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Build and install OpenMC executable + Python API
RUN git clone https://github.com/openmc-dev/openmc.git /opt/openmc \
    && mkdir /opt/openmc/build \
    && cd /opt/openmc/build \
    && cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local \
    && make -j4 \
    && make install \
    && pip install /opt/openmc

# Install extra Python dependencies
RUN pip install --no-cache-dir numpy matplotlib

# Set the working directory inside the container
WORKDIR /app

# Default command
CMD ["python", "/app/Code/12.py"]
