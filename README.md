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

# Installation Guide: IAN-R1-openmc Model
Follow these steps to run the IAN-R1-openmc model directly on your computer.

Step 1: Install Docker and Git
Make sure you have Docker and Git installed. If not, download it from the official Docker website https://www.docker.com/get-started/ and Git from https://git-scm.com/downloads

Step 2: Clone the Repository
First, open your terminal and clone the GitHub project.

```bash

git clone https://github.com/sohhae/IAN-R1-openmc.git
cd IAN-R1-openmc
```
Step 3: Build the Docker Image
This command builds the Docker image, which installs Python, OpenMC, and all other dependencies inside the container. this step might take some minutes

```bash
docker build -t ian-r1-openmc 
```
Step 4: Activate the Virtual Environment
To run the model, use the following command. This command mounts your entire project folder inside the container so the code can access all necessary files and save results.

```bash
docker run --rm -it -v "$(pwd)":/app ian-r1-openmc python /app/Code/main_model.py
```
