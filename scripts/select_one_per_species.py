#!/usr/bin/env python3

import re
import sys
from Bio import SeqIO

def extract_species_name(header):
    """Extract species name from FASTA header"""
    # Match patterns like "Campylobacter coli" or "Campylobacter jejuni"
    match = re.search(r'([A-Z][a-z]+ [a-z]+)', header)
    if match:
        return match.group(1)
    return None

def select_one_per_species(input_file, output_file):
    """Select one sequence per species from a FASTA file"""
    seen_species = set()
    selected_records = []
    
    # Read all sequences from the input file
    records = list(SeqIO.parse(input_file, "fasta"))
    
    for record in records:
        species = extract_species_name(record.description)
        if species and species not in seen_species:
            seen_species.add(species)
            selected_records.append(record)
    
    # Write selected sequences to output file
    SeqIO.write(selected_records, output_file, "fasta")
    
    print(f"Found {len(seen_species)} unique species.")
    print(f"Selected {len(selected_records)} sequences out of {len(records)} total.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python select_one_per_species.py input.fasta output.fasta")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    select_one_per_species(input_file, output_file)