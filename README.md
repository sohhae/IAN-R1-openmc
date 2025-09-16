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

Step 1: Install Git
If you do not have Git installed, you'll need to download and install it first to clone the repository. Go to https://git-scm.com/downloads and follow the installation instructions for your operating system. After installation, restart your terminal.

Step 2: Clone the Repository
First, open your terminal and clone the GitHub project.

```bash

git clone https://github.com/sohhae/IAN-R1-openmc.git
cd IAN-R1-openmc
```
Step 3: Create a Python Virtual Environment
It is a good practice to create a virtual environment to isolate project dependencies and avoid conflicts with other Python installations.

```bash
python3 -m venv venv
```
Step 4: Activate the Virtual Environment
Activate the virtual environment you just created. The commands vary depending on your operating system:

On macOS and Linux:

```bash
source venv/bin/activate
```
On Windows:

```bash
venv\Scripts\activate
```
Step 5: Install Dependencies
Once the virtual environment is active, install all the necessary libraries using the project's requirements.txt file.

```bash
pip install -r requirements.txt
```
Step 6: Run the Main Model
Now you can run the model's main script. Make sure your terminal is in the project's root directory (IAN-R1-openmc).

```bash
python Code/main_model.py
```
That's it! The model will run and the results will be saved in the Results/ folder of your project.
