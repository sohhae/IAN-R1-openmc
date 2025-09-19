FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gfortran \
    cmake \
    git \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir numpy matplotlib \
    && pip install --no-cache-dir git+https://github.com/openmc-dev/openmc.git

WORKDIR /app

CMD ["python", "/app/Code/main_model.py"]
