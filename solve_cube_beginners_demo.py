#!/usr/bin/env python
"""
Rubik's Cube Demo: Instantiate, Scramble, and Solve using Beginner's Algorithm

This script demonstrates:
1. Creating a solved Rubik's Cube
2. Scrambling it with random moves
3. Solving it using the Beginner's method
"""

from rubik_solver.Cubie import Cube
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Printer import TtyPrinter

def main():
    print("=" * 60)
    print("RUBIK'S CUBE SOLVER DEMONSTRATION")
    print("Using Beginner's Algorithm")
    print("=" * 60)
    print()
    
    # Step 1: Instantiate a solved cube
    print("Step 1: Creating a solved Rubik's Cube...")
    cube = Cube()
    print("✓ Cube created successfully!")
    print()
    
    # Display the solved cube
    print("Initial State (SOLVED):")
    printer = TtyPrinter(cube, colours=True)
    printer.pprint()
    print()
    
    # Step 2: Scramble the cube
    print("Step 2: Scrambling the cube...")
    scramble_moves = cube.shuffle(seed=42)
    print(f"✓ Cube scrambled with {len(scramble_moves)} random moves!")
    print(f"Scramble sequence: {', '.join(map(str, scramble_moves[:20]))}...")
    print()
    
    # Display the scrambled cube
    print("Scrambled State:")
    printer = TtyPrinter(cube, colours=True)
    printer.pprint()
    print()
    
    # Step 3: Solve the cube using Beginner's algorithm
    print("Step 3: Solving the cube using Beginner's Algorithm...")
    solver = BeginnerSolver(cube)
    solution_moves = solver.solution()
    print(f"✓ Solution found with {len(solution_moves)} moves!")
    print()
    
    # Display the solution
    print("Solution sequence:")
    print(', '.join(map(str, solution_moves)))
    print()
    
    # Step 4: Apply the solution to verify
    print("Step 4: Applying solution moves to verify...")
    for move in solution_moves:
        cube.move(move)
    print("✓ All solution moves applied!")
    print()
    
    # Display the final (solved) cube
    print("Final State (SOLVED):")
    printer = TtyPrinter(cube, colours=True)
    printer.pprint()
    print()
    
    print("=" * 60)
    print("SUCCESS! The cube has been solved using the Beginner's Algorithm!")
    print("=" * 60)

if __name__ == "__main__":
    main()
