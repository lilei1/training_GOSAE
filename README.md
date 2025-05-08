# GOSAE: Genome Ocean Sparse Autoencoder

This repository contains scripts and tools for training and evaluating a Sparse Autoencoder (SAE) approach to extract genomic features from biological sequence data.

## Overview

GOSAE (Genome Ocean Sparse Autoencoder) is designed to:
1. Extract meaningful features from genomic sequences
2. Interpret functional significance of these features
3. Support the GenomeOcean platform for biological data analysis

## Data Processing Pipeline

The repository includes scripts for:

- Removing duplicate sequences (`scripts/remove_duplicates.py`)
- Selecting representative sequences per species (`scripts/select_one_per_species.py`)
- Splitting data into training and validation sets (`scripts/split_train_val.py`)

## Usage

### Data Preparation

1. Remove duplicates from your FASTA files:
   ```
   python scripts/remove_duplicates.py input.fasta deduplicated.fasta
   ```

2. Select one sequence per species (optional):
   ```
   python scripts/select_one_per_species.py deduplicated.fasta representative.fasta
   ```

3. Split into training and validation sets:
   ```
   python scripts/split_train_val.py deduplicated.fasta train.fasta val.fasta --ratio 0.7
   ```

### Training

[Training instructions to be added]

### Evaluation

[Evaluation instructions to be added]

## Requirements

- Python 3.6+
- BioPython
- [Other dependencies]

## Citation

If you use this code in your research, please cite:
[Citation information to be added]
