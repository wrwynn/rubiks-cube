#!/usr/bin/env python
"""
3D Rubik's Cube Visualization

This script creates an interactive 3D visualization of a Rubik's Cube
using matplotlib. You can view the cube from different angles and see
how it looks after scrambling.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from rubik_solver.Cubie import Cube

# Color mapping for cube faces
COLOR_MAP = {
    'R': '#FF0000',  # Red
    'O': '#FF8800',  # Orange
    'B': '#0000FF',  # Blue
    'G': '#00FF00',  # Green
    'W': '#FFFFFF',  # White
    'Y': '#FFFF00',  # Yellow
    '.': '#888888',  # Gray (placeholder)
}

def get_cube_face_positions():
    """
    Returns the 3D positions for each sticker on the cube.
    Each face has 9 stickers (3x3 grid).
    """
    positions = {}
    
    # Define the center positions for each of the 6 faces
    # Front face (F) - facing +Z
    positions['F'] = []
    for i in range(3):
        for j in range(3):
            x = -1 + j
            y = 1 - i
            positions['F'].append((x, y, 1.5, 'F'))
    
    # Back face (B) - facing -Z
    positions['B'] = []
    for i in range(3):
        for j in range(3):
            x = 1 - j
            y = 1 - i
            positions['B'].append((x, y, -1.5, 'B'))
    
    # Right face (R) - facing +X
    positions['R'] = []
    for i in range(3):
        for j in range(3):
            z = 1 - j
            y = 1 - i
            positions['R'].append((1.5, y, z, 'R'))
    
    # Left face (L) - facing -X
    positions['L'] = []
    for i in range(3):
        for j in range(3):
            z = -1 + j
            y = 1 - i
            positions['L'].append((-1.5, y, z, 'L'))
    
    # Up face (U) - facing +Y
    positions['U'] = []
    for i in range(3):
        for j in range(3):
            x = -1 + j
            z = 1 - i
            positions['U'].append((x, 1.5, z, 'U'))
    
    # Down face (D) - facing -Y
    positions['D'] = []
    for i in range(3):
        for j in range(3):
            x = -1 + j
            z = -1 + i
            positions['D'].append((x, -1.5, z, 'D'))
    
    return positions

def draw_sticker(ax, center, normal, color, size=0.5):
    """
    Draw a single sticker (small square) on the cube face.
    """
    x, y, z = center
    
    # Create the vertices of the sticker based on the normal direction
    if normal == 'F':  # Front face (+Z)
        vertices = [
            [x - size, y - size, z],
            [x + size, y - size, z],
            [x + size, y + size, z],
            [x - size, y + size, z]
        ]
    elif normal == 'B':  # Back face (-Z)
        vertices = [
            [x - size, y - size, z],
            [x + size, y - size, z],
            [x + size, y + size, z],
            [x - size, y + size, z]
        ]
    elif normal == 'R':  # Right face (+X)
        vertices = [
            [x, y - size, z - size],
            [x, y + size, z - size],
            [x, y + size, z + size],
            [x, y - size, z + size]
        ]
    elif normal == 'L':  # Left face (-X)
        vertices = [
            [x, y - size, z - size],
            [x, y + size, z - size],
            [x, y + size, z + size],
            [x, y - size, z + size]
        ]
    elif normal == 'U':  # Up face (+Y)
        vertices = [
            [x - size, y, z - size],
            [x + size, y, z - size],
            [x + size, y, z + size],
            [x - size, y, z + size]
        ]
    elif normal == 'D':  # Down face (-Y)
        vertices = [
            [x - size, y, z - size],
            [x + size, y, z - size],
            [x + size, y, z + size],
            [x - size, y, z + size]
        ]
    else:
        # Default case (should not happen)
        vertices = [
            [x - size, y - size, z],
            [x + size, y - size, z],
            [x + size, y + size, z],
            [x - size, y + size, z]
        ]
    
    # Create the polygon
    poly = Poly3DCollection([vertices])
    poly.set_facecolor(color)
    poly.set_edgecolor('black')
    poly.set_linewidth(2)
    ax.add_collection3d(poly)

def visualize_cube(cube, title="Rubik's Cube 3D Visualization"):
    """
    Create a 3D visualization of the Rubik's Cube.
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get the cube configuration
    naive_cube = cube.to_naive_cube()
    cube_string = naive_cube.get_cube()
    
    # Map cube string positions to face positions
    # The cube_string has 54 characters representing all stickers
    # Order: U(0-8), L(9-17), F(18-26), R(27-35), B(36-44), D(45-53)
    face_indices = {
        'U': list(range(0, 9)),
        'L': list(range(9, 18)),
        'F': list(range(18, 27)),
        'R': list(range(27, 36)),
        'B': list(range(36, 45)),
        'D': list(range(45, 54))
    }
    
    # Get positions for all stickers
    positions = get_cube_face_positions()
    
    # Draw each sticker
    for face in ['F', 'B', 'R', 'L', 'U', 'D']:
        face_positions = positions[face]
        indices = face_indices[face]
        
        for i, (x, y, z, normal) in enumerate(face_positions):
            color_char = cube_string[indices[i]].upper()
            color = COLOR_MAP.get(color_char, '#888888')
            draw_sticker(ax, (x, y, z), normal, color)
    
    # Set the aspect ratio and limits
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    
    # Set title
    ax.set_title(title, fontsize=16, fontweight='bold')
    
    # Remove axis lines, labels, and ticks
    ax.set_axis_off()
    
    # Set initial viewing angle
    ax.view_init(elev=20, azim=45)
    
    return fig, ax

def main():
    print("=" * 60)
    print("3D RUBIK'S CUBE VISUALIZATION")
    print("=" * 60)
    print()
    
    # Create a solved cube
    print("Creating a solved cube...")
    cube = Cube()
    
    print("Displaying solved cube in 3D...")
    fig1, ax1 = visualize_cube(cube, "Solved Rubik's Cube")
    
    # Scramble the cube
    print("\nScrambling the cube with 20 moves...")
    scramble_moves = cube.shuffle(seed=42)
    print(f"Scramble: {', '.join(map(str, scramble_moves[:20]))}")
    
    print("\nDisplaying scrambled cube in 3D...")
    fig2, ax2 = visualize_cube(cube, "Scrambled Rubik's Cube")
    
    print("\n" + "=" * 60)
    print("3D visualizations created!")
    print("You can rotate the view by clicking and dragging.")
    print("Close the windows to exit.")
    print("=" * 60)
    
    plt.show()

if __name__ == "__main__":
    main()
