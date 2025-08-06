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

    # Find the "Final metrics:" section - look for the line and capture everything after it
    # Use a more flexible pattern that can handle multiline JSON
    pattern = r"Final metrics:\s*(\{.*)"
    match = re.search(pattern, log_content, re.DOTALL)

    if not match:
        raise ValueError("Could not find 'Final metrics:' in the log file")

    # Extract the JSON string - it should be the rest of the line/file after "Final metrics:"
    metrics_str = match.group(1).strip()

    # Handle potential issues with the JSON format
    try:
        # Try direct parsing first
        metrics_dict = json.loads(metrics_str)
    except json.JSONDecodeError:
        try:
            # If direct parsing fails, try to clean the string
            # This handles potential issues with Python literal representation
            metrics_str_cleaned = metrics_str.replace("'", '"')  # Replace single quotes with double quotes
            metrics_dict = json.loads(metrics_str_cleaned)
        except json.JSONDecodeError:
            # If JSON parsing still fails, try to evaluate as Python literal
            import ast
            try:
                metrics_dict = ast.literal_eval(metrics_str)
            except (ValueError, SyntaxError) as e:
                raise ValueError(f"Could not parse metrics data. Original error: {e}\nExtracted string: {metrics_str[:200]}...")

    return metrics_dict

def plot_metrics(metrics, output_file='training_metrics.pdf'):
    """
    Plot the metrics extracted from the log file.

    Args:
        metrics: Dictionary containing the metrics to plot
        output_file: Path to save the plot
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

    # Calculate appropriate y-axis limits based on actual data
    all_sparsities = train_sparsities + val_sparsities
    min_sparsity = min(all_sparsities)
    max_sparsity = max(all_sparsities)
    sparsity_range = max_sparsity - min_sparsity

    # Add some padding to the y-axis limits
    y_min = max(0, min_sparsity - 0.1 * sparsity_range)
    y_max = min(1, max_sparsity + 0.1 * sparsity_range)
    ax2.set_ylim(y_min, y_max)

    # Add reference line for target sparsity if it's within the visible range
    target_sparsity = 0.01  # Based on your training parameters
    if y_min <= target_sparsity <= y_max:
        ax2.axhline(y=target_sparsity, color='red', linestyle='--', alpha=0.7, label=f'Target Sparsity ({target_sparsity})')

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
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.show()

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract and plot training metrics from log file.')
    parser.add_argument('log_file', help='Path to the training log file')
    parser.add_argument('--output', '-o', default='training_metrics.pdf',
                        help='Output file name for the plot (default: training_metrics.pdf)')

    args = parser.parse_args()

    try:
        print(f"Reading log file: {args.log_file}")

        # Extract metrics from the log file
        metrics = extract_metrics_from_log(args.log_file)

        print(f"Successfully extracted metrics:")
        print(f"  - Training epochs: {len(metrics['train_losses'])}")
        print(f"  - Validation points: {len(metrics['val_losses'])}")
        print(f"  - Sparsity range: {min(metrics['train_sparsities']):.4f} - {max(metrics['train_sparsities']):.4f}")

        # Plot the metrics
        plot_metrics(metrics, args.output)

        print(f"Plot saved as: {args.output}")
        print("Metrics successfully extracted and plotted!")

    except FileNotFoundError:
        print(f"Error: Log file '{args.log_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()