#!/usr/bin/env python3

# this file is AI generated

"""Simple visualization script for timing data"""
import csv
import sys
from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("matplotlib not found. Install with: pip install matplotlib")

def print_stats(csv_file):
    """Print statistics from CSV"""
    import os
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        print("\nTo generate timing data:")
        print("  1. Start the server: ./server")
        print("  2. Run benchmark: ./benchmark.sh")
        print("  3. Then run this script again")
        return
    
    data = defaultdict(list)
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row['label']
            time_ms = float(row['time_ms'])
            data[label].append(time_ms)
    
    print("\n" + "="*60)
    print("PERFORMANCE STATISTICS")
    print("="*60)
    
    for label, times in data.items():
        if times:
            avg = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            print(f"\n{label}:")
            print(f"  Count:    {len(times)}")
            print(f"  Average:  {avg:.3f} ms")
            print(f"  Min:      {min_time:.3f} ms")
            print(f"  Max:      {max_time:.3f} ms")
    
    print("="*60 + "\n")

def plot_graph(csv_file, output_file="timings.png"):
    """Create a simple bar chart"""
    if not HAS_MATPLOTLIB:
        print("Cannot create graph without matplotlib")
        return
    
    data = defaultdict(list)
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row['label']
            time_ms = float(row['time_ms'])
            data[label].append(time_ms)
    
    labels = []
    averages = []
    
    for label, times in data.items():
        if times:
            labels.append(label)
            averages.append(sum(times) / len(times))
    
    plt.figure(figsize=(10, 6))
    plt.bar(labels, averages, color=['#4CAF50', '#2196F3'])
    plt.ylabel('Time (ms)')
    plt.title('Average Response Times')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    csv_file = "timings.csv"
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    import os
    if not os.path.exists(csv_file):
        print_stats(csv_file)  # This will print the error message
        sys.exit(1)
    
    print_stats(csv_file)
    
    if HAS_MATPLOTLIB:
        plot_graph(csv_file)
    else:
        print("\nTo generate a graph, install matplotlib:")
        print("  pip install matplotlib")

