#!/usr/bin/env python3

import sys
import argparse
from Bio import SeqIO
from Bio.Seq import Seq

def remove_duplicates(input_file, output_file, method="sequence"):
    """
    Remove duplicate sequences from a FASTA file
    
    Parameters:
    - input_file: Path to input FASTA file
    - output_file: Path to output FASTA file
    - method: Method to identify duplicates:
              "sequence" - exact sequence match (default)
              "id" - identical sequence IDs
              "both" - either sequence or ID match
    """
    records = list(SeqIO.parse(input_file, "fasta"))
    print(f"Read {len(records)} sequences from {input_file}")
    
    # Track what we've seen before
    seen_sequences = set()
    seen_ids = set()
    unique_records = []
    
    for record in records:
        # Convert sequence to string for comparison
        seq_str = str(record.seq).upper()  # Convert to uppercase for case-insensitive comparison
        
        # Check if this is a duplicate based on the chosen method
        is_duplicate = False
        
        if method == "sequence" or method == "both":
            if seq_str in seen_sequences:
                is_duplicate = True
            else:
                seen_sequences.add(seq_str)
                
        if method == "id" or method == "both":
            if record.id in seen_ids:
                is_duplicate = True
            else:
                seen_ids.add(record.id)
        
        # If not a duplicate, keep it
        if not is_duplicate:
            unique_records.append(record)
    
    # Write the unique records to the output file
    SeqIO.write(unique_records, output_file, "fasta")
    
    print(f"Removed {len(records) - len(unique_records)} duplicate sequences")
    print(f"Wrote {len(unique_records)} unique sequences to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove duplicate sequences from a FASTA file.')
    parser.add_argument('input', help='Input FASTA file')
    parser.add_argument('output', help='Output FASTA file')
    parser.add_argument('--method', choices=['sequence', 'id', 'both'], default='sequence',
                        help='Method to identify duplicates: sequence (default), id, or both')
    
    args = parser.parse_args()
    
    remove_duplicates(args.input, args.output, args.method)