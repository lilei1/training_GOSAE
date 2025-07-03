#!/usr/bin/env python3

"""
Filter FASTA sequences by length range
Author: Li Lei
Date: 2025-07-03

This script filters sequences from a FASTA file based on a specified length range
and reports the number of sequences selected.
"""

import argparse
import sys
from Bio import SeqIO

def filter_sequences_by_length(input_file, output_file, min_length, max_length):
    """
    Filter sequences from a FASTA file based on length range
    
    Parameters:
    - input_file: Path to input FASTA file
    - output_file: Path to output FASTA file
    - min_length: Minimum sequence length (inclusive)
    - max_length: Maximum sequence length (inclusive)
    
    Returns:
    - Number of sequences selected
    """
    selected_records = []
    total_sequences = 0
    
    # Read sequences and filter by length
    for record in SeqIO.parse(input_file, "fasta"):
        total_sequences += 1
        seq_length = len(record.seq)
        
        # Check if sequence length is within the specified range
        if min_length <= seq_length <= max_length:
            selected_records.append(record)
    
    # Write selected sequences to output file
    SeqIO.write(selected_records, output_file, "fasta")
    
    # Report results
    selected_count = len(selected_records)
    print(f"Total sequences processed: {total_sequences}")
    print(f"Sequences selected (length {min_length}-{max_length} bp): {selected_count}")
    print(f"Percentage selected: {(selected_count/total_sequences)*100:.2f}%")
    print(f"Output written to: {output_file}")
    
    return selected_count

def main():
    parser = argparse.ArgumentParser(
        description='Filter FASTA sequences by length range',.././test/NonBLA/filted_Non_BLA_sequence.fasta
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python filter_sequences_by_length.py input.fasta output.fasta --min 201 --max 133342
  python filter_sequences_by_length.py input.fasta output.fasta -m 500 -M 2000
        """
    )
    
    parser.add_argument('input', help='Input FASTA file')
    parser.add_argument('output', help='Output FASTA file for filtered sequences')
    parser.add_argument('--min', '-m', type=int, required=True,
                        help='Minimum sequence length (inclusive)')
    parser.add_argument('--max', '-M', type=int, required=True,
                        help='Maximum sequence length (inclusive)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.min < 0:
        print("Error: Minimum length cannot be negative")
        sys.exit(1)
    
    if args.max < args.min:
        print("Error: Maximum length cannot be less than minimum length")
        sys.exit(1)
    
    try:
        # Filter sequences
        selected_count = filter_sequences_by_length(
            args.input, args.output, args.min, args.max
        )
        
        if selected_count == 0:
            print("Warning: No sequences found within the specified length range")
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
