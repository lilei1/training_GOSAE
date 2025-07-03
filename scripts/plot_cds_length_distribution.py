#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import numpy as np
from Bio import SeqIO
import seaborn as sns

def analyze_cds_lengths(fasta_file, output_plot=None, bins=50):
    """
    Calculate CDS lengths from a FASTA file and plot their distribution
    
    Parameters:
    - fasta_file: Path to input FASTA file containing CDS sequences
    - output_plot: Path to save the plot (if None, plot will be displayed)
    - bins: Number of bins for the histogram
    """
    # Read sequences and calculate lengths
    lengths = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        lengths.append(len(record.seq))
    
    # Calculate statistics
    total_seqs = len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    mean_length = np.mean(lengths)
    median_length = np.median(lengths)
    
    # Print statistics
    print(f"Total sequences: {total_seqs}")
    print(f"Minimum length: {min_length} bp")
    print(f"Maximum length: {max_length} bp")
    print(f"Mean length: {mean_length:.2f} bp")
    print(f"Median length: {median_length:.2f} bp")
    
    # Set up the plot style
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Create the histogram
    sns.histplot(lengths, bins=bins, kde=True)
    
    # Add vertical lines for mean and median
    plt.axvline(mean_length, color='red', linestyle='--', label=f'Mean: {mean_length:.2f} bp')
    plt.axvline(median_length, color='green', linestyle='--', label=f'Median: {median_length:.2f} bp')
    
    # Set plot labels and title
    plt.xlabel('CDS Length (bp)')
    plt.ylabel('Frequency')
    plt.title('Distribution of CDS Lengths')
    plt.legend()
    
    # Save or display the plot
    if output_plot:
        plt.savefig(output_plot, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {output_plot}")
    else:
        plt.show()
    
    return lengths, {'total': total_seqs, 'min': min_length, 'max': max_length, 
                    'mean': mean_length, 'median': median_length}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze and plot CDS length distribution from a FASTA file.')
    parser.add_argument('input', help='Input FASTA file containing CDS sequences')
    parser.add_argument('--output', help='Output file for the plot (PNG, PDF, etc.)')
    parser.add_argument('--bins', type=int, default=50, help='Number of bins for the histogram (default: 50)')
    
    args = parser.parse_args()
    
    analyze_cds_lengths(args.input, args.output, args.bins)