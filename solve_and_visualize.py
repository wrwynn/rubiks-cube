#!/usr/bin/env python
"""
Rubik's Cube: Solve and Visualize

This script combines the solving algorithms with 3D visualization,
showing the cube before and after solving.
"""

import matplotlib.pyplot as plt
from rubik_solver.Cubie import Cube
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Solver.CFOP import CFOPSolver
from rubik_solver.Solver.Kociemba import KociembaSolver
from visualize_cube_3d import visualize_cube

def main():
    print("=" * 70)
    print("RUBIK'S CUBE: SOLVE AND VISUALIZE")
    print("=" * 70)
    print()
    
    # Create and scramble a cube
    print("Step 1: Creating and scrambling a Rubik's Cube...")
    cube = Cube()
    scramble_moves = cube.shuffle(seed=123)
    print(f"✓ Cube scrambled with {len(scramble_moves)} moves")
    print(f"   First 20 moves: {', '.join(map(str, scramble_moves[:20]))}...")
    print()
    
    # Visualize scrambled cube
    print("Step 2: Visualizing the scrambled cube...")
    fig_scrambled, _ = visualize_cube(cube, "Scrambled Cube")
    plt.pause(0.1)  # Brief pause to display
    print("✓ Scrambled cube displayed")
    print()
    
    # Choose solving method
    print("Step 3: Choose solving algorithm:")
    print("   1. Beginner's Algorithm (simple, ~180 moves)")
    print("   2. CFOP Algorithm (intermediate, ~110 moves)")
    print("   3. Kociemba Algorithm (optimal, ~20 moves)")
    print()
    
    # For automation, we'll solve with all three methods
    methods = [
        ("Beginner", BeginnerSolver),
        ("CFOP", CFOPSolver),
        ("Kociemba", KociembaSolver)
    ]
    
    solutions = {}
    
    for method_name, solver_class in methods:
        print(f"Solving with {method_name}...")
        test_cube = Cube()
        # Apply same scramble
        for move in scramble_moves:
            test_cube.move(move)
        
        solver = solver_class(test_cube)
        if method_name == "Kociemba":
            solution = solver.solution(maxDepth=23, timeOut=100)
        else:
            solution = solver.solution()
        
        solutions[method_name] = len(solution)
        print(f"   ✓ {method_name}: {len(solution)} moves")
    
    print()
    print("Solution Comparison:")
    print("-" * 40)
    for method, moves in solutions.items():
        print(f"   {method:15s}: {moves:3d} moves")
    print("-" * 40)
    print()
    
    # Solve with Kociemba (most efficient)
    print("Step 4: Solving with Kociemba's algorithm...")
    solver = KociembaSolver(cube)
    solution_moves = solver.solution(maxDepth=23, timeOut=100)
    print(f"✓ Solution found: {', '.join(map(str, solution_moves))}")
    print()
    
    # Apply solution
    print("Step 5: Applying solution...")
    for move in solution_moves:
        cube.move(move)
    print("✓ Solution applied")
    print()
    
    # Visualize solved cube
    print("Step 6: Visualizing the solved cube...")
    fig_solved, _ = visualize_cube(cube, "Solved Cube")
    print("✓ Solved cube displayed")
    print()
    
    print("=" * 70)
    print("SUCCESS!")
    print(f"The cube was scrambled with {len(scramble_moves)} moves")
    print(f"and solved in just {len(solution_moves)} moves using Kociemba's algorithm!")
    print()
    print("Interact with the 3D visualizations:")
    print("  • Click and drag to rotate the view")
    print("  • Scroll to zoom in/out")
    print("  • Close windows to exit")
    print("=" * 70)
    
    plt.show()

if __name__ == "__main__":
    main()
