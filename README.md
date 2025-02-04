# Project Title
Thank you for your interest in our project! This repository contains all necessary files and scripts to perform molecular simulations and subsequent analyses for our hydrophobic polymer / excipient systems. Below, you'll find an overview of the repository structure and how to get started.

## Citation
If you use this repository in your research, please cite the following preprint:

J. W. P. Zajac, P. Muralikrishnan, C. L. Heldt, S. L. Perry, and S. Sarupria (2024) Impact of Co-Excipient Selection on Hydrophobic Polymer Folding: Insights for Optimal Formulation Design. arXiv:2407.00885 [cond-mat.soft]

## Repository Structure

### **Simulations** (`simulations/`)
This directory contains all files required to set up and run molecular dynamics (MD) simulations. It is organized into the following subdirectories:

- **`mdp/`** – Stores MD parameter files (`.mdp`) defining simulation settings.
- **`mdrun/`** – Scripts and configurations for executing MD runs.
- **`topol/`** – Topology files (`.top`, `.itp`) describing molecular structures and interactions.
- **`box-solv/`** – Scripts and files for defining the simulation box and solvating the system.
- **`insert-molecules/`** – Scripts for inserting excipient molecules into the simulation box.
- **`gen-ions/`** – Configuration files for adding ions to neutralize the system.
- **`reus/`** - Scripts and tools used to run REUS simulations via PLUMED.
- **`ndx/`** - All index files generated to aid in energy group definitions or analysis.
- **`conf/`** - Initial configurations used for simulations.

### **Analysis** (`analysis/`)
This directory contains scripts and tools for post-simulation analysis, including structure validation, energy calculations, and trajectory processing.

- **`centrality/`** - Tools for computing network centrality measures.
- **`fragmentation/`** - Scripts for analyzing local solvent network fragmentation.
- **`gyrate/`** - Computes hydrophobic polymer radius of gyration.
- **`preferentialInteraction/`** - Evaluation of preferential interaction coefficients between polymer-excipient.
- **`trjconv/`** - Utilities for trajectory conversions and modifications.
- **`waterReorientation/`** - Analysis of hydration shell water reorientation dynamics.

## Getting Started
To use this repository:
1. Clone the repository:
   ```bash
   git clone git@github.com:SAMPEL-Group/Hydrophobic-Polymer-Binary-Excipients.git
   cd Hydrophobic-Polymer-Binary-Excipients
   ```
2. Navigate to the relevant directory and follow the provided instructions.
3. Ensure dependencies (e.g., GROMACS, Python libraries) are installed as needed.

## Contributions
Contributions are welcome! Please submit a pull request or open an issue if you have suggestions or improvements.

## License
All written and graphical materials here are made available under a CC-BY 4.0 license, and all source code/software is made available under an MIT license. Both of these allow broad reuse with attribution.

## Contact
For questions or feedback, please contact Jonathan Zajac at zajac028@umn.edu.
