#!/usr/bin/env python3

import sys
import random
import argparse
from Bio import SeqIO

'''
This script subset 25% of the data and then splits a FASTA file into two subsets based on a given ratio.
The subset and split are done randomly, and the random seed can be specified for reproducibility.
'''

def subset_and_split(input_file, subset_file, subset_ratio, split_file1, split_file2, split_ratio, seed=42):
    """
    Subset and split sequences from a FASTA file
    
    Parameters:
    - input_file: Path to input FASTA file
    - subset_file: Path to output subset FASTA file
    - subset_ratio: Fraction of sequences for the subset (default: 0.25)
    - split_file1: Path to output split file 1
    - split_file2: Path to output split file 2
    - split_ratio: Fraction of sequences for split file 1 (default: 0.5)
    - seed: Random seed for reproducibility
    """
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Read all sequences
    records = list(SeqIO.parse(input_file, "fasta"))
    total_count = len(records)
    
    # Shuffle the records
    random.shuffle(records)
    
    # Calculate subset size
    subset_count = int(total_count * subset_ratio)
    
    # Subset the records
    subset_records = records[:subset_count]
    remaining_records = records[subset_count:]
    
    # Write subset to output file
    SeqIO.write(subset_records, subset_file, "fasta")
    
    # Calculate split size for subset records
    split_count = int(len(subset_records) * split_ratio)
    
    # Split the subset records
    split_records1 = subset_records[:split_count]
    split_records2 = subset_records[split_count:]
    
    # Write split records to output files
    SeqIO.write(split_records1, split_file1, "fasta")
    SeqIO.write(split_records2, split_file2, "fasta")
    
    print(f"Total sequences: {total_count}")
    print(f"Subset sequences: {len(subset_records)} ({subset_ratio*100:.1f}%)")
    print(f"Split 1 sequences (from subset): {len(split_records1)} ({split_ratio*100:.1f}%)")
    print(f"Split 2 sequences (from subset): {len(split_records2)} ({(1-split_ratio)*100:.1f}%)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Subset and split FASTA sequences.')
    parser.add_argument('input', help='Input FASTA file')
    parser.add_argument('subset', help='Output subset FASTA file')
    parser.add_argument('split1', help='Output split 1 FASTA file')
    parser.add_argument('split2', help='Output split 2 FASTA file')
    parser.add_argument('--subset_ratio', type=float, default=0.25, 
                        help='Fraction of sequences for the subset (default: 0.25)')
    parser.add_argument('--split_ratio', type=float, default=0.5, 
                        help='Fraction of remaining sequences for split 1 (default: 0.5)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility (default: 42)')
    
    args = parser.parse_args()
    
    subset_and_split(args.input, args.subset, args.subset_ratio, args.split1, args.split2, args.split_ratio, args.seed) 

    