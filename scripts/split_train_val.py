#!/usr/bin/env python3

import sys
import random
import argparse
from Bio import SeqIO

def split_sequences(input_file, train_file, val_file, split_ratio=0.5, seed=42):
    """
    Split sequences from a FASTA file into training and validation sets
    
    Parameters:
    - input_file: Path to input FASTA file with deduplicated sequences
    - train_file: Path to output training set FASTA file
    - val_file: Path to output validation set FASTA file
    - split_ratio: Fraction of sequences for training (default: 0.5)
    - seed: Random seed for reproducibility
    """
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Read all sequences
    records = list(SeqIO.parse(input_file, "fasta"))
    total_count = len(records)
    
    # Shuffle the records
    random.shuffle(records)
    
    # Calculate split point
    train_count = int(total_count * split_ratio)
    
    # Split the records
    train_records = records[:train_count]
    val_records = records[train_count:]
    
    # Write to output files
    SeqIO.write(train_records, train_file, "fasta")
    SeqIO.write(val_records, val_file, "fasta")
    
    print(f"Total sequences: {total_count}")
    print(f"Training sequences: {len(train_records)} ({split_ratio*100:.1f}%)")
    print(f"Validation sequences: {len(val_records)} ({(1-split_ratio)*100:.1f}%)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split FASTA sequences into training and validation sets.')
    parser.add_argument('input', help='Input FASTA file with deduplicated sequences')
    parser.add_argument('train', help='Output training set FASTA file')
    parser.add_argument('val', help='Output validation set FASTA file')
    parser.add_argument('--ratio', type=float, default=0.5, 
                        help='Fraction of sequences for training (default: 0.5)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility (default: 42)')
    
    args = parser.parse_args()
    
    split_sequences(args.input, args.train, args.val, args.ratio, args.seed)