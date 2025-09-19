FROM python:3.11-slim

WORKDIR /app

# Install all system dependencies required to build and run OpenMC
RUN apt-get update && apt-get install -y \
    gfortran \
    libopenmpi-dev \
    openmpi-bin \
    cmake \
    git \
    libhdf5-dev \
    libpng-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Clone OpenMC and build from source
RUN git clone https://github.com/openmc-dev/openmc.git /opt/openmc && \
    mkdir /opt/openmc/build && \
    cd /opt/openmc/build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make -j4 && \
    make install

# Install Python API and other project dependencies
COPY requirements.txt ./ 
RUN pip install --no-cache-dir /opt/openmc && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set the default command to run your main script
CMD ["python", "Code/12.py"]





