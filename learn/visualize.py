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
            # Skip if this is the header row or invalid data
            if 'label' not in row or 'time_ms' not in row:
                continue
            if row['label'] == 'label' or row['time_ms'] == 'time_ms':
                continue
            try:
                label = row['label']
                time_ms = float(row['time_ms'])
                data[label].append(time_ms)
            except (ValueError, KeyError):
                continue  # Skip invalid rows
    
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

def plot_graph(csv_file, output_file=None):
    if output_file is None:
        output_file = "timings.png"
    """Create a simple bar chart"""
    if not HAS_MATPLOTLIB:
        print("Cannot create graph without matplotlib")
        return
    
    data = defaultdict(list)
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip if this is the header row or invalid data
            if 'label' not in row or 'time_ms' not in row:
                continue
            if row['label'] == 'label' or row['time_ms'] == 'time_ms':
                continue
            try:
                label = row['label']
                time_ms = float(row['time_ms'])
                data[label].append(time_ms)
            except (ValueError, KeyError):
                continue  # Skip invalid rows
    
    # Map labels to descriptive names and order
    label_map = {
        "direct processing": "Direct Processing\n(no scheduler)",
        "worker task": "Worker Processing\n(with scheduler)",
        "end-to-end RPC": "End-to-End RPC\n(with scheduler)"
    }
    
    # Order: direct, worker, end-to-end
    label_order = ["direct processing", "worker task", "end-to-end RPC"]
    
    labels = []
    display_labels = []
    averages = []
    colors = []
    
    for label in label_order:
        if label in data and data[label]:
            labels.append(label)
            display_labels.append(label_map.get(label, label))
            avg = sum(data[label]) / len(data[label])
            averages.append(avg)
            # Color: green for direct, blue for worker, orange for end-to-end
            if label == "direct processing":
                colors.append('#4CAF50')  # Green
            elif label == "worker task":
                colors.append('#2196F3')  # Blue
            else:
                colors.append('#FF9800')  # Orange
    
    # Add any remaining labels not in order
    for label, times in data.items():
        if label not in label_order and times:
            labels.append(label)
            display_labels.append(label_map.get(label, label))
            averages.append(sum(times) / len(times))
            colors.append('#9E9E9E')  # Gray
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(display_labels, averages, color=colors)
    plt.ylabel('Time (ms)', fontsize=12)
    plt.title('Scheduler Performance: Direct vs Scheduler Comparison', fontsize=14, pad=20, fontweight='bold')
    
    # Add value labels on bars
    for bar, avg in zip(bars, averages):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{avg:.4f} ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Calculate and show overhead/benefits
    if "direct processing" in data and "end-to-end RPC" in data:
        direct_avg = sum(data["direct processing"]) / len(data["direct processing"])
        rpc_avg = sum(data["end-to-end RPC"]) / len(data["end-to-end RPC"])
        overhead = rpc_avg - direct_avg
        overhead_pct = (overhead / direct_avg) * 100 if direct_avg > 0 else 0
        
        # Determine if scheduler is beneficial
        worker_avg = sum(data.get("worker task", [0])) / len(data.get("worker task", [1]))
        work_time = worker_avg if worker_avg > 0 else direct_avg
        
        # If work time is significant, overhead is acceptable
        if work_time > 0.01:  # If work takes > 0.01ms, scheduler overhead is reasonable
            benefit_msg = f"✓ Scheduler overhead ({overhead:.4f} ms) is {overhead/work_time*100:.1f}% of work time - acceptable for queuing/control benefits"
            color = 'lightgreen'
        else:
            benefit_msg = f"⚠ Scheduler adds {overhead:.4f} ms overhead ({overhead_pct:.1f}% slower) - useful for complex tasks, queuing, and resource control"
            color = 'wheat'
        
        # Add annotation
        plt.figtext(0.5, 0.05, 
                    f'{benefit_msg} | '
                    'Direct = no scheduler, Worker = actual work, End-to-End = total with scheduler',
                    ha='center', fontsize=10, style='italic',
                    bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
    
    plt.xticks(rotation=0, ha='center', fontsize=11)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.18)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    csv_file = "timings.csv"
    output_file = None
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    import os
    if not os.path.exists(csv_file):
        print_stats(csv_file)  # This will print the error message
        sys.exit(1)
    
    print_stats(csv_file)
    
    if HAS_MATPLOTLIB:
        plot_graph(csv_file, output_file)
    else:
        print("\nTo generate a graph, install matplotlib:")
        print("  pip install matplotlib")

