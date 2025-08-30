# IAN-R1-openmc
# Overview
This repository contains an OpenMC model of the IAN-R1 research reactor. The IAN-R1 is a pool-type, light-water moderated and cooled reactor located at the Instituto de Asuntos Nucleares in Bogotá, Colombia. Commissioned in 1965, the unit operates at a rated thermal power of 30 kW for research, isotope production, and academic training.
The purpose of this repository is to replicate the IAN-R1 geometry, materials, and operating conditions in OpenMC, achieving the highest possible fidelity, and to provide a reusable and documented model for research and educational purposes.

![633f9ceb2f2b4](https://github.com/user-attachments/assets/36b78e1a-e0e6-452a-96fb-03339ac49e2b)
Figure 1: Picture of the AIN-R1

# Project Goals
* Build a high-fidelity IAN-R1 reactor core model in OpenMC
* Document the **geometry, materials, and configuration** of the reactor.  
* Provide a **reproducible setup** for students and researchers.  
* Generate **visualizations** of the reactor core (fuel, control rods, irradiation channels)
  
# Repository Structure
- `/Code`: Main source of code and plotters 
- `/Results`: Simulation outputs and visual images 
- `.gitignore`: Ignore rules (prevents heavy OpenMC files like `.h5` from being uploaded)  
- `.gitattributes`: Configuration file for Git LFS (Large File Storage, e.g. for `.h5` if tracked)  
- `README.md`: Project description and usage instructions

# Installation Guide - Dockers
These steps show you how to run the IAN-R1-openmc model using Docker.

1. Make sure you have Dockerinstalled.
2. Clone the IAN-R1-openmc repository from GitHub:
```bash
git clone https://github.com/sohhae/IAN-R1-openmc.git
cd IAN-R1-openmc
```

3. Build the Docker image (this will install Python, OpenMC, and all dependencies inside the container):
```bash
docker build -t ian-r1-openmc .
```

4. Run the main model inside the container (simulation outputs will appear in the Results/ folder):
```bash
docker run --rm -it -v $(pwd)/Results:/app/Results ian-r1-openmc
```

5. You can also run plotting scripts directly inside the container:
```bash
docker run --rm -it -v $(pwd)/Results:/app/Results ian-r1-openmc python "Code/3D Plot Top.py"
docker run --rm -it -v $(pwd)/Results:/app/Results ian-r1-openmc python "Code/3D Plot XZ.py"
```
