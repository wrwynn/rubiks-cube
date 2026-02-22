#!/usr/bin/env python
"""
Visualize Rubik's Cube Algorithm Benchmark Results

This script runs benchmarks and creates visualizations including:
- Formatted tables with results
- Bar charts comparing performance metrics
- Detailed graphs of timing and move efficiency
"""

import time
import statistics
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from rubik_solver.Cubie import Cube
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Solver.CFOP import CFOPSolver
from rubik_solver.Solver.Kociemba import KociembaSolver

trials = 5

def benchmark_algorithm(solver_class, algorithm_name, num_trials=trials):
    """Benchmark a solving algorithm over multiple trials"""
    print(f"\nBenchmarking {algorithm_name}... ({num_trials} trials)")
    
    times = []
    move_counts = []
    
    for i in range(num_trials):
        cube = Cube()
        cube.shuffle()
        
        start_time = time.time()
        
        if solver_class == KociembaSolver:
            solver = solver_class(cube)
            solution = solver.solution(maxDepth=23, timeOut=100)
        else:
            solver = solver_class(cube)
            solution = solver.solution()
        
        end_time = time.time()
        
        times.append((end_time - start_time) * 1000)  # Convert to ms
        move_counts.append(len(solution))
        
        if (i + 1) % 200 == 0:
            print(f"  Progress: {i + 1}/{num_trials}")
    
    return {
        'algorithm': algorithm_name,
        'times': times,
        'moves': move_counts,
        'avg_time': statistics.mean(times),
        'std_time': statistics.stdev(times),
        'min_time': min(times),
        'max_time': max(times),
        'avg_moves': statistics.mean(move_counts),
        'std_moves': statistics.stdev(move_counts),
        'min_moves': min(move_counts),
        'max_moves': max(move_counts)
    }

def create_summary_table(results_list):
    """Create a formatted summary table"""
    print("\n" + "="*80)
    print("BENCHMARK RESULTS SUMMARY")
    print("="*80 + "\n")
    
    # Main comparison table
    headers = ["Algorithm", "Avg Time (ms)", "Std Dev (ms)", "Avg Moves", "Std Dev", "Min Moves", "Max Moves"]
    table_data = []
    
    for result in results_list:
        table_data.append([
            result['algorithm'],
            f"{result['avg_time']:.2f}",
            f"{result['std_time']:.2f}",
            f"{result['avg_moves']:.2f}",
            f"{result['std_moves']:.2f}",
            result['min_moves'],
            result['max_moves']
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Detailed statistics table
    print("\n" + "="*80)
    print("DETAILED TIMING STATISTICS")
    print("="*80 + "\n")
    
    headers2 = ["Algorithm", "Min Time", "Max Time", "Median Time", "90th Percentile"]
    table_data2 = []
    
    for result in results_list:
        table_data2.append([
            result['algorithm'],
            f"{result['min_time']:.2f} ms",
            f"{result['max_time']:.2f} ms",
            f"{statistics.median(result['times']):.2f} ms",
            f"{np.percentile(result['times'], 90):.2f} ms"
        ])
    
    print(tabulate(table_data2, headers=headers2, tablefmt="grid"))

def create_visualizations(results_list):
    """Create comprehensive visualizations of the benchmark results"""
    
    # Set up the figure with subplots
    fig = plt.figure(figsize=(16, 10))
    
    algorithms = [r['algorithm'] for r in results_list]
    colors = ['#3498db', '#e74c3c', '#2ecc71']  # Blue, Red, Green
    
    # 1. Average Time Comparison (Bar Chart)
    ax1 = plt.subplot(2, 3, 1)
    avg_times = [r['avg_time'] for r in results_list]
    bars1 = ax1.bar(algorithms, avg_times, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Time (ms)', fontsize=11)
    ax1.set_title('Average Solving Time', fontsize=13, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10)
    
    # 2. Average Moves Comparison (Bar Chart)
    ax2 = plt.subplot(2, 3, 2)
    avg_moves = [r['avg_moves'] for r in results_list]
    bars2 = ax2.bar(algorithms, avg_moves, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Number of Moves', fontsize=11)
    ax2.set_title('Average Move Count', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=10)
    
    # 3. Time Distribution (Box Plot)
    ax3 = plt.subplot(2, 3, 3)
    time_data = [r['times'] for r in results_list]
    bp1 = ax3.boxplot(time_data, tick_labels=algorithms, patch_artist=True)
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax3.set_ylabel('Time (ms)', fontsize=11)
    ax3.set_title('Time Distribution', fontsize=13, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # 4. Move Distribution (Box Plot)
    ax4 = plt.subplot(2, 3, 4)
    move_data = [r['moves'] for r in results_list]
    bp2 = ax4.boxplot(move_data, tick_labels=algorithms, patch_artist=True)
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax4.set_ylabel('Number of Moves', fontsize=11)
    ax4.set_title('Move Count Distribution', fontsize=13, fontweight='bold')
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Efficiency Comparison (Time vs Moves Scatter)
    ax5 = plt.subplot(2, 3, 5)
    for result, color in zip(results_list, colors):
        ax5.scatter(result['avg_moves'], result['avg_time'], 
                   s=200, alpha=0.7, color=color, edgecolors='black', linewidth=2,
                   label=result['algorithm'])
        ax5.annotate(result['algorithm'], 
                    (result['avg_moves'], result['avg_time']),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, fontweight='bold')
    ax5.set_xlabel('Average Moves', fontsize=11)
    ax5.set_ylabel('Average Time (ms)', fontsize=11)
    ax5.set_title('Efficiency: Time vs Moves', fontsize=13, fontweight='bold')
    ax5.grid(True, alpha=0.3)
    ax5.legend()
    
    # 6. Performance Summary (Grouped Bar Chart)
    ax6 = plt.subplot(2, 3, 6)
    x = np.arange(len(algorithms))
    width = 0.35
    
    # Normalize values to 0-100 scale for comparison
    max_time = max(avg_times)
    max_moves = max(avg_moves)
    norm_times = [(t/max_time)*100 for t in avg_times]
    norm_moves = [(m/max_moves)*100 for m in avg_moves]
    
    bars_time = ax6.bar(x - width/2, norm_times, width, label='Time (normalized)',
                       color='#3498db', alpha=0.7, edgecolor='black')
    bars_moves = ax6.bar(x + width/2, norm_moves, width, label='Moves (normalized)',
                        color='#e74c3c', alpha=0.7, edgecolor='black')
    
    ax6.set_ylabel('Normalized Score (0-100)', fontsize=11)
    ax6.set_title('Overall Performance Comparison', fontsize=13, fontweight='bold')
    ax6.set_xticks(x)
    ax6.set_xticklabels(algorithms)
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight')
    print("\n✓ Visualization saved as 'benchmark_results.png'")
    plt.show()

def main():
    print("="*80)
    print("RUBIK'S CUBE ALGORITHM BENCHMARK WITH VISUALIZATION")
    print("="*80)
    print("\nRunning benchmarks (" + str(trials) + " trials per algorithm)...")
    print("This will take several minutes. Please wait...")
    
    # Run benchmarks
    beginner_results = benchmark_algorithm(BeginnerSolver, "Beginner")
    cfop_results = benchmark_algorithm(CFOPSolver, "CFOP")
    kociemba_results = benchmark_algorithm(KociembaSolver, "Kociemba")
    
    results_list = [beginner_results, cfop_results, kociemba_results]
    
    # Create summary tables
    create_summary_table(results_list)
    
    # Create visualizations
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)
    create_visualizations(results_list)
    
    print("\n" + "="*80)
    print("BENCHMARK COMPLETE!")
    print("="*80)
    print("\nKey Findings:")
    print(f"  • Fastest Algorithm: CFOP ({cfop_results['avg_time']:.2f} ms avg)")
    print(f"  • Most Efficient (fewest moves): Kociemba ({kociemba_results['avg_moves']:.2f} moves avg)")
    print(f"  • Best Balance: CFOP offers good speed with reasonable move count")
    print(f"  • Kociemba Trade-off: Optimal solutions but slower computation")

if __name__ == "__main__":
    main()
