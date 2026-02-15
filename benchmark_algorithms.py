#!/usr/bin/env python
"""
Benchmark Rubik's Cube Solving Algorithms

This script runs the three solving algorithms (Beginner, CFOP, Kociemba)
1000 times each to measure their performance in terms of:
- Average solving time
- Average number of moves
- Standard deviation
"""

import time
import statistics
from rubik_solver.Cubie import Cube
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Solver.CFOP import CFOPSolver
from rubik_solver.Solver.Kociemba import KociembaSolver

def benchmark_algorithm(solver_class, algorithm_name, num_trials=5):
    """
    Benchmark a solving algorithm over multiple trials
    
    Args:
        solver_class: The solver class to test
        algorithm_name: Name of the algorithm for display
        num_trials: Number of times to run the algorithm
    
    Returns:
        Dictionary with timing and move count statistics
    """
    print(f"\n{'='*60}")
    print(f"Benchmarking {algorithm_name} Algorithm")
    print(f"Running {num_trials} trials...")
    print(f"{'='*60}")
    
    times = []
    move_counts = []
    
    for i in range(num_trials):
        # Create and scramble a new cube for each trial
        cube = Cube()
        cube.shuffle()
        
        # Time the solving process
        start_time = time.time()
        
        if solver_class == KociembaSolver:
            solver = solver_class(cube)
            solution = solver.solution(maxDepth=23, timeOut=100)
        else:
            solver = solver_class(cube)
            solution = solver.solution()
        
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        move_counts.append(len(solution))
        
        # Progress indicator every 100 trials
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{num_trials} trials completed...")
    
    # Calculate statistics
    results = {
        'algorithm': algorithm_name,
        'avg_time': statistics.mean(times),
        'std_time': statistics.stdev(times),
        'min_time': min(times),
        'max_time': max(times),
        'avg_moves': statistics.mean(move_counts),
        'std_moves': statistics.stdev(move_counts),
        'min_moves': min(move_counts),
        'max_moves': max(move_counts),
        'total_time': sum(times)
    }
    
    return results

def print_results(results):
    """Print benchmark results in a formatted way"""
    print(f"\n{'='*60}")
    print(f"RESULTS: {results['algorithm']}")
    print(f"{'='*60}")
    print(f"Total execution time: {results['total_time']:.2f} seconds")
    print(f"\nTiming Statistics:")
    print(f"  Average time:  {results['avg_time']*1000:.2f} ms")
    print(f"  Std deviation: {results['std_time']*1000:.2f} ms")
    print(f"  Min time:      {results['min_time']*1000:.2f} ms")
    print(f"  Max time:      {results['max_time']*1000:.2f} ms")
    print(f"\nMove Count Statistics:")
    print(f"  Average moves: {results['avg_moves']:.2f}")
    print(f"  Std deviation: {results['std_moves']:.2f}")
    print(f"  Min moves:     {results['min_moves']}")
    print(f"  Max moves:     {results['max_moves']}")
    print(f"{'='*60}")

def main():
    print("*" * 60)
    print("RUBIK'S CUBE ALGORITHM BENCHMARK")
    print("Testing: Beginner, CFOP, and Kociemba Algorithms")
    print("Number of trials: 1000 per algorithm")
    print("*" * 60)
    
    # Benchmark Beginner Algorithm
    beginner_results = benchmark_algorithm(BeginnerSolver, "Beginner")
    print_results(beginner_results)
    
    # Benchmark CFOP Algorithm
    cfop_results = benchmark_algorithm(CFOPSolver, "CFOP")
    print_results(cfop_results)
    
    # Benchmark Kociemba Algorithm
    kociemba_results = benchmark_algorithm(KociembaSolver, "Kociemba")
    print_results(kociemba_results)
    
    # Print comparison summary
    print(f"\n{'='*60}")
    print("COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"\n{'Algorithm':<15} {'Avg Time (ms)':<15} {'Avg Moves':<15}")
    print(f"{'-'*45}")
    print(f"{'Beginner':<15} {beginner_results['avg_time']*1000:<15.2f} {beginner_results['avg_moves']:<15.2f}")
    print(f"{'CFOP':<15} {cfop_results['avg_time']*1000:<15.2f} {cfop_results['avg_moves']:<15.2f}")
    print(f"{'Kociemba':<15} {kociemba_results['avg_time']*1000:<15.2f} {kociemba_results['avg_moves']:<15.2f}")
    print(f"{'='*60}")
    
    # Determine winners
    fastest_time = min(beginner_results['avg_time'], cfop_results['avg_time'], kociemba_results['avg_time'])
    fewest_moves = min(beginner_results['avg_moves'], cfop_results['avg_moves'], kociemba_results['avg_moves'])
    
    print(f"\nFastest Algorithm (by time): ", end="")
    if beginner_results['avg_time'] == fastest_time:
        print("Beginner")
    elif cfop_results['avg_time'] == fastest_time:
        print("CFOP")
    else:
        print("Kociemba")
    
    print(f"Most Efficient (by moves): ", end="")
    if beginner_results['avg_moves'] == fewest_moves:
        print("Beginner")
    elif cfop_results['avg_moves'] == fewest_moves:
        print("CFOP")
    else:
        print("Kociemba")
    
    print(f"\n{'='*60}")
    print("BENCHMARK COMPLETE!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
