#!/usr/bin/env python3
import re
import json
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

def extract_metrics_from_log(log_file_path):
    """
    Extract the 'Final metrics:' data from a log file.
    
    Args:
        log_file_path: Path to the log file
        
    Returns:
        Dictionary containing the extracted metrics
    """
    with open(log_file_path, 'r') as file:
        log_content = file.read()
    
    # Find the "Final metrics:" section using a non-greedy regex
    pattern = r"Final metrics: (\{.*?\})"
    match = re.search(pattern, log_content, re.DOTALL)
    
    if not match:
        raise ValueError("Could not find 'Final metrics:' in the log file")
    
    # Extract the JSON string and parse it
    metrics_str = match.group(1)
    
    # Handle potential issues with the JSON format
    try:
        # Try direct parsing
        metrics_dict = json.loads(metrics_str)
    except json.JSONDecodeError:
        # If direct parsing fails, try to clean the string
        # This handles potential issues with Python literal representation
        metrics_str = metrics_str.replace("'", '"')  # Replace single quotes with double quotes
        metrics_dict = json.loads(metrics_str)
    
    return metrics_dict

def plot_metrics(metrics):
    """
    Plot the metrics extracted from the log file.
    
    Args:
        metrics: Dictionary containing the metrics to plot
    """
    # Extract data from the metrics dictionary
    train_losses = metrics['train_losses']
    val_losses = metrics['val_losses']
    train_sparsities = metrics['train_sparsities']
    val_sparsities = metrics['val_sparsities']
    dead_neurons = metrics['dead_neurons']
    
    # Create x-axis values
    train_epochs = list(range(1, len(train_losses) + 1))
    val_epochs = np.linspace(1, len(train_losses), len(val_losses))
    
    # Create a figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
    
    # Plot 1: Training and Validation Losses
    ax1.plot(train_epochs, train_losses, 'b-', marker='o', markersize=3, label='Training Loss')
    ax1.plot(val_epochs, val_losses, 'r-', marker='s', markersize=5, label='Validation Loss')
    ax1.set_title('Training and Validation Losses Over Time', fontsize=14)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.set_yscale('log')  # Log scale helps visualize the decreasing trend better
    ax1.grid(True, which="both", ls="--", alpha=0.7)
    ax1.legend(fontsize=10)
    
    # Plot 2: Training and Validation Sparsities
    ax2.plot(train_epochs, train_sparsities, 'g-', marker='o', markersize=3, label='Training Sparsity')
    ax2.plot(val_epochs, val_sparsities, 'purple', marker='s', markersize=5, label='Validation Sparsity')
    ax2.set_title('Training and Validation Sparsities Over Time', fontsize=14)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Sparsity', fontsize=12)
    ax2.axhline(y=0.5, color='gray', linestyle='--', label='Ideal Sparsity (0.5)')
    ax2.set_ylim(0.48, 0.52)  # Limit y-axis to better visualize changes around 0.5
    ax2.grid(True, alpha=0.7)
    ax2.legend(fontsize=10)
    
    # Plot 3: Dead Neurons
    ax3.plot(train_epochs, dead_neurons, 'r-', marker='x', markersize=5)
    ax3.set_title('Dead Neurons Over Time', fontsize=14)
    
    ax3.set_xlabel('Epoch', fontsize=12)
    ax3.set_ylabel('Number of Dead Neurons', fontsize=12)
    ax3.grid(True, alpha=0.7)
    ax3.set_ylim(-0.5, max(dead_neurons) + 1 if max(dead_neurons) > 0 else 1)  # Set reasonable y-limits
    
    plt.tight_layout()
    plt.savefig('training_metrics.pdf')
    plt.show()

# Main execution
if __name__ == "__main__":
    # Replace with your log file path
    log_file_path = sys.argv[1]
    
    try:
        # Extract metrics from the log file
        metrics = extract_metrics_from_log(log_file_path)
        
        # Plot the metrics
        plot_metrics(metrics)
        
        print("Metrics successfully extracted and plotted!")
    except Exception as e:
        print(f"Error: {e}")