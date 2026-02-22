#!/usr/bin/env python
"""
Rubik's Cube: Solve and Visualize

This script combines the solving algorithms with 3D visualization,
showing the cube before and after solving.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from rubik_solver.Cubie import Cube
from rubik_solver.Solver.Beginner import BeginnerSolver
from rubik_solver.Solver.CFOP import CFOPSolver
from rubik_solver.Solver.Kociemba import KociembaSolver
import math
import time

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
    """Returns the 3D positions for each sticker on the cube."""
    positions = {}
    
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

def get_rotation_matrix(axis, angle):
    """Get 3D rotation matrix for rotating around an axis."""
    angle_rad = math.radians(angle)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    
    if axis == 'x':
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    elif axis == 'y':
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    elif axis == 'z':
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return np.eye(3)

def rotate_point_around_center(point, axis, angle, center):
    """Rotate a 3D point around an axis passing through center using matrix."""
    point_arr = np.array(point) - np.array(center)
    rot_matrix = get_rotation_matrix(axis, angle)
    rotated = rot_matrix @ point_arr
    return tuple(rotated + np.array(center))

def get_face_center(face):
    """Get the center point of a face for rotation."""
    centers = {
        'R': (1.5, 0, 0),
        'L': (-1.5, 0, 0),
        'U': (0, 1.5, 0),
        'D': (0, -1.5, 0),
        'F': (0, 0, 1.5),
        'B': (0, 0, -1.5),
    }
    return centers.get(face, (0, 0, 0))

def determine_new_normal(x, y, z):
    """Determine which face normal a rotated vector corresponds to."""
    # Find the closest matching face normal
    normals = {
        'F': (0, 0, 1),
        'B': (0, 0, -1),
        'R': (1, 0, 0),
        'L': (-1, 0, 0),
        'U': (0, 1, 0),
        'D': (0, -1, 0),
    }
    
    max_dot = -float('inf')
    best_face = 'F'
    
    for face, normal in normals.items():
        # Normalize the rotated vector
        length = math.sqrt(x*x + y*y + z*z)
        if length > 0.0001:
            nx, ny, nz = x/length, y/length, z/length
        else:
            nx, ny, nz = 0, 0, 1
        
        # Dot product with each normal
        dot = nx * normal[0] + ny * normal[1] + nz * normal[2]
        if dot > max_dot:
            max_dot = dot
            best_face = face
    
    return best_face

def rotate_sticker_vertices(center, normal, axis, angle):
    """Rotate sticker vertices around the sticker's own center while also rotating position."""
    size = 0.5
    
    # Get the rotated center position
    face_center_map = {'R': (1.5, 0, 0), 'L': (-1.5, 0, 0), 'U': (0, 1.5, 0),
                      'D': (0, -1.5, 0), 'F': (0, 0, 1.5), 'B': (0, 0, -1.5)}
    
    # Find which face we're rotating around based on axis
    if axis == 'x':
        moving_face = 'R'  # x-axis = R face rotation
    elif axis == 'y':
        moving_face = 'U'  # y-axis = U face rotation  
    else:
        moving_face = 'F'  # z-axis = F face rotation
    
    face_center = face_center_map.get(moving_face, (0, 0, 0))
    
    # Rotate the center position around the face center
    new_center = rotate_point_around_center(center, axis, angle, face_center)
    
    return new_center

def draw_sticker(ax, center, normal, color, size=0.5):
    """Draw a single sticker on the cube face."""
    x, y, z = center
    
    # Get vertices for each face orientation based on normal direction
    if normal == 'F':
        # Front face - square in XY plane at z
        verts = np.array([
            [x - size, y - size, z],
            [x + size, y - size, z],
            [x + size, y + size, z],
            [x - size, y + size, z]
        ])
    elif normal == 'B':
        # Back face - square in XY plane at z (flipped)
        verts = np.array([
            [x + size, y - size, z],
            [x - size, y - size, z],
            [x - size, y + size, z],
            [x + size, y + size, z]
        ])
    elif normal == 'R':
        # Right face - square in YZ plane at x
        verts = np.array([
            [x, y - size, z - size],
            [x, y + size, z - size],
            [x, y + size, z + size],
            [x, y - size, z + size]
        ])
    elif normal == 'L':
        # Left face - square in YZ plane at x (flipped)
        verts = np.array([
            [x, y + size, z - size],
            [x, y - size, z - size],
            [x, y - size, z + size],
            [x, y + size, z + size]
        ])
    elif normal == 'U':
        # Up face - square in XZ plane at y
        verts = np.array([
            [x - size, y, z - size],
            [x + size, y, z - size],
            [x + size, y, z + size],
            [x - size, y, z + size]
        ])
    elif normal == 'D':
        # Down face - square in XZ plane at y (flipped)
        verts = np.array([
            [x - size, y, z + size],
            [x + size, y, z + size],
            [x + size, y, z - size],
            [x - size, y, z - size]
        ])
    else:
        # Default - Front face
        verts = np.array([
            [x - size, y - size, z],
            [x + size, y - size, z],
            [x + size, y + size, z],
            [x - size, y + size, z]
        ])
    
    poly = Poly3DCollection([verts])
    poly.set_facecolor(color)
    poly.set_edgecolor('black')
    poly.set_linewidth(2)
    ax.add_collection3d(poly)

def get_rotating_layer_info(face):
    """Get axis and which stickers rotate for a face move."""
    # Axis of rotation for each face
    axis_map = {'R': 'x', 'L': 'x', 'U': 'y', 'D': 'y', 'F': 'z', 'B': 'z'}
    axis = axis_map.get(face, 'x')
    
    # Get all sticker positions that rotate with this face
    # Each face has 9 stickers, plus 3 from each of 4 adjacent faces = 21 total
    rotating_stickers = []  # List of (face, sticker_index)
    
    # The face itself (9 stickers)
    for i in range(9):
        rotating_stickers.append((face, i))
    
    # Adjacent face edge stickers
    if face == 'R':
        # Right face: U right column, F right column, D right column, B left column (reversed)
        for i in [2, 5, 8]:
            rotating_stickers.append(('U', i))
            rotating_stickers.append(('F', i))
            rotating_stickers.append(('D', i))
        for i in [6, 3, 0]:  # B left column reversed
            rotating_stickers.append(('B', i))
    elif face == 'L':
        for i in [0, 3, 6]:
            rotating_stickers.append(('U', i))
            rotating_stickers.append(('F', i))
            rotating_stickers.append(('D', i))
        for i in [8, 5, 2]:  # B right column reversed
            rotating_stickers.append(('B', i))
    elif face == 'U':
        for i in [0, 1, 2]:
            rotating_stickers.append(('F', i))
            rotating_stickers.append(('B', i))
            rotating_stickers.append(('R', i))
            rotating_stickers.append(('L', i))
    elif face == 'D':
        for i in [6, 7, 8]:
            rotating_stickers.append(('F', i))
            rotating_stickers.append(('B', i))
            rotating_stickers.append(('R', i))
            rotating_stickers.append(('L', i))
    elif face == 'F':
        for i in [6, 7, 8]:  # U bottom row
            rotating_stickers.append(('U', i))
        for i in [2, 1, 0]:  # D top row reversed
            rotating_stickers.append(('D', i))
        for i in [0, 3, 6]:  # R left column
            rotating_stickers.append(('R', i))
        for i in [8, 5, 2]:  # L right column reversed
            rotating_stickers.append(('L', i))
    elif face == 'B':
        for i in [2, 1, 0]:  # U top row reversed
            rotating_stickers.append(('U', i))
        for i in [6, 7, 8]:  # D bottom row
            rotating_stickers.append(('D', i))
        for i in [2, 5, 8]:  # R right column
            rotating_stickers.append(('R', i))
        for i in [0, 3, 6]:  # L left column reversed
            rotating_stickers.append(('L', i))
    
    return axis, rotating_stickers

def animate_move(ax, cube, move, positions, face_indices):
    """Animate a single move with proper rotation."""
    move_str = str(move)
    clean_move = move_str.replace("'", "").replace("2", "")
    face = clean_move[0]
    
    # Determine rotation parameters
    if move_str.endswith("2"):
        num_steps = 2
        direction = 1
    elif move_str.endswith("'"):
        num_steps = 1
        direction = 1
    else:
        num_steps = 1
        direction = -1
    
    axis, rotating_stickers = get_rotating_layer_info(face)
    total_angle = 90 * num_steps * direction
    
    # Get cube state BEFORE move (this is key!)
    naive_cube_before = cube.to_naive_cube()
    cube_string_before = naive_cube_before.get_cube()
    
    # Apply the actual move to get state AFTER
    cube.move(move)
    naive_cube_after = cube.to_naive_cube()
    cube_string_after = naive_cube_after.get_cube()
    
    # Animate the rotation
    num_animation_steps = 10
    for step in range(num_animation_steps + 1):
        angle = (total_angle * step) / num_animation_steps
        ax.clear()
        
        # Draw all stickers
        for draw_face in ['F', 'B', 'R', 'L', 'U', 'D']:
            face_positions = positions[draw_face]
            indices = face_indices[draw_face]
            
            for i, (x, y, z, normal) in enumerate(face_positions):
                # Check if this sticker is in the rotating layer
                is_rotating = (draw_face, i) in rotating_stickers
                
                if is_rotating:
                    # This sticker rotates - use color from BEFORE state
                    color_char = cube_string_before[indices[i]].upper()
                    color = COLOR_MAP.get(color_char, '#888888')
                    
                    # Rotate the position around face center
                    face_center = get_face_center(face)
                    rx, ry, rz = rotate_point_around_center((x, y, z), axis, angle, face_center)
                    
                    # Also rotate the normal to match the new orientation
                    # Get the original normal vector
                    normal_vec = {'F': (0, 0, 1), 'B': (0, 0, -1), 'R': (1, 0, 0), 
                                 'L': (-1, 0, 0), 'U': (0, 1, 0), 'D': (0, -1, 0)}.get(normal, (0, 0, 1))
                    rxn, ryn, rzn = rotate_point_around_center(normal_vec, axis, angle, (0, 0, 0))
                    
                    # Determine new normal based on rotated direction
                    new_normal = determine_new_normal(rxn, ryn, rzn)
                    
                    # Also rotate the sticker around its OWN center
                    # Get the sticker's original center
                    sticker_center = (x, y, z)
                    # Rotate around face center to get new position
                    new_center = rotate_point_around_center(sticker_center, axis, angle, face_center)
                    # Rotate the sticker vertices around its own center
                    rx, ry, rz = rotate_sticker_vertices((x, y, z), new_normal, axis, angle)
                    draw_sticker(ax, (rx, ry, rz), new_normal, color)
                else:
                    # Static sticker - use AFTER state (unchanged by this move)
                    color_char = cube_string_after[indices[i]].upper()
                    color = COLOR_MAP.get(color_char, '#888888')
                    draw_sticker(ax, (x, y, z), normal, color)
        
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.set_box_aspect([1, 1, 1])
        ax.set_axis_off()
        ax.view_init(elev=35, azim=-45)
        plt.pause(0.02)
    
    plt.pause(0.05)

def draw_cube_state_final(ax, cube_string, positions, face_indices):
    """Draw the cube without rotation."""
    ax.clear()
    
    for face in ['F', 'B', 'R', 'L', 'U', 'D']:
        face_positions = positions[face]
        indices = face_indices[face]
        
        for i, (x, y, z, normal) in enumerate(face_positions):
            color_char = cube_string[indices[i]].upper()
            color = COLOR_MAP.get(color_char, '#888888')
            draw_sticker(ax, (x, y, z), normal, color)
    
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_box_aspect([1, 1, 1])
    ax.set_axis_off()
    ax.view_init(elev=35, azim=-45)

def update_cube_visualization(ax, cube, title, positions, face_indices):
    """Update the cube visualization with new cube state."""
    naive_cube = cube.to_naive_cube()
    cube_string = naive_cube.get_cube()
    draw_cube_state_final(ax, cube_string, positions, face_indices)
    ax.set_title(title, fontsize=16, fontweight='bold')

def get_solver_choice():
    """Prompt user to choose which solver to use."""
    print("=" * 70)
    print("CHOOSE YOUR SOLVER")
    print("=" * 70)
    print()
    print("Available solvers:")
    print("  1. Beginner   - Good for learning, step-by-step approach")
    print("  2. CFOP       - Speedcubing method, popular and efficient")
    print("  3. Kociemba   - Most efficient, computer-optimized solution")
    print()
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            return 'beginner'
        elif choice == '2':
            return 'cfop'
        elif choice == '3':
            return 'kociemba'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    print("=" * 70)
    print("RUBIK'S CUBE: SOLVE AND VISUALIZE")
    print("=" * 70)
    print()
    
    # Get solver choice from user
    solver_choice = get_solver_choice()
    solver_names = {
        'beginner': "Beginner's algorithm",
        'cfop': 'CFOP method',
        'kociemba': 'Kociemba algorithm'
    }
    print(f"You selected: {solver_names[solver_choice]}")
    print()
    
    # Create and scramble a cube
    print("Step 1: Creating and scrambling a Rubik's Cube...")
    cube = Cube()
    scramble_moves = cube.shuffle(seed=123)
    print(f"✓ Cube scrambled with {len(scramble_moves)} moves")
    print()
    
    # Pre-compute positions and face indices
    positions = get_cube_face_positions()
    face_indices = {
        'U': list(range(0, 9)),
        'L': list(range(9, 18)),
        'F': list(range(18, 27)),
        'R': list(range(27, 36)),
        'B': list(range(36, 45)),
        'D': list(range(45, 54))
    }
    
    # Also need rotate_point function (old one for compatibility)
    def rotate_point(point, axis, angle):
        """Rotate a 3D point around origin by given angle (for backwards compatibility)."""
        x, y, z = point
        angle_rad = math.radians(angle)
        
        if axis == 'x':
            cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
            return (x, y * cos_a - z * sin_a, y * sin_a + z * cos_a)
        elif axis == 'y':
            cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
            return (x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a)
        elif axis == 'z':
            cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
            return (x * cos_a - y * sin_a, x * sin_a + y * cos_a, z)
        return point
    
    # Create figure for animation
    print("Step 2: Creating animated visualization...")
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Visualize scrambled cube first
    update_cube_visualization(ax, cube, "Scrambled Cube", positions, face_indices)
    plt.pause(0.5)
    print("✓ Scrambled cube displayed")
    print()
    
    # Solve with selected solver
    print(f"Step 3: Solving with {solver_names[solver_choice]}...")
    
    if solver_choice == 'beginner':
        solver = BeginnerSolver(cube)
        solution_moves = solver.solution()
    elif solver_choice == 'cfop':
        solver = CFOPSolver(cube)
        solution_moves = solver.solution()
    elif solver_choice == 'kociemba':
        solver = KociembaSolver(cube)
        solution_moves = solver.solution()
    
    print(f"✓ Solution found: {len(solution_moves)} moves")
    print()
    
    # Animate the solution - show each move step by step with stopwatch
    print("Step 4: Animating the solution step by step...")
    print("   (Watch the cube solve in real-time!)")
    print()
    
    # Start the stopwatch
    start_time = time.time()
    
    for i, move in enumerate(solution_moves):
        # Apply move to cube
        cube.move(move)
        # Calculate elapsed time
        elapsed = time.time() - start_time
        # Format time as MM:SS.ms
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        time_str = f"{minutes:02d}:{seconds:05.2f}"
        # Update and show visualization with stopwatch
        title = f"Solving with {solver_names[solver_choice]}... Move {i+1}/{len(solution_moves)}: {move} | Time: {time_str}"
        update_cube_visualization(ax, cube, title, positions, face_indices)
        plt.pause(0.02)  # Pause to see each move
    
    # Final solved state
    update_cube_visualization(ax, cube, "Solved Cube!", positions, face_indices)
    print("✓ Solution animated!")
    print()
    
    print("=" * 70)
    print("SUCCESS!")
    print(f"The cube was scrambled with {len(scramble_moves)} moves")
    print(f"and solved in {len(solution_moves)} moves using {solver_names[solver_choice]}!")
    print()
    print("Interact with the 3D visualization:")
    print("  • Click and drag to rotate the view")
    print("  • Scroll to zoom in/out")
    print("  • Close window to exit")
    print("=" * 70)
    
    plt.show()

if __name__ == "__main__":
    main()
