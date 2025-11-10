from collections import deque
import time
import tracemalloc as tm
from maze_object import Maze
from maze_layouts import mazes
from maze_layouts import optimal_path_length

def get_neighbors(pos, maze):
    """
    Finds valid neighboring positions (up, down, left, right) that are not walls.

    Args:
        pos (tuple): The current (row, column) position.
        maze (list of lists): The 2D grid representing the maze.
                              '1' usually means a path/open space.
                              '10' likely represents the goal/end position.

    Returns:
        list: A list of valid (row, column) neighbor positions.
    """
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and (maze[nr][nc] == 1 or maze[nr][nc] == 10):
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(came_from, current):
    """
    Reconstructs the path from the start position to the 'current' position
    using the 'came_from' dictionary.

    Args:
        came_from (dict): Maps a position (key) to the position from which
                          it was first reached (value).
        current (tuple): The goal position (or the last position visited if no path was found).

    Returns:
        list: The shortest path from start to 'current' (excluding 'current' if it's the goal).
    """
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def breadth_first_search(maze_object):
    """
    Performs Breadth-First Search (BFS) to find the shortest path from start to goal 
    in the provided maze.

    Args:
        maze_object (Maze): An object containing the maze grid, start, and end positions.

    Returns:
        tuple: (path, visited, success) 
               path (list): The reconstructed path (list of positions).
               visited (set): All positions explored during the search.
               success (bool): True if a path to the goal was found, False otherwise.
    """
    maze = maze_object.maze
    start = maze_object.start_pos
    goal = maze_object.end_pos
    
    success = False
    
    frontier = deque([start])
    came_from = {start: None}
    visited = set({start})

    while frontier:
        current = frontier.popleft()

        if current == goal:
            success = True
            return reconstruct_path(came_from, current), visited, success

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
                came_from[neighbor] = current
    
    return reconstruct_path(came_from, current), visited, success

# Iterate through all mazes defined in maze_layouts.mazes.
for i in range(len(mazes)):
    maze_num = i+1
    maze = Maze(maze_num)

    start_time = time.time()
    tm.start()
    path, visited, success = breadth_first_search(maze)
    end_time = time.time()
    current_memory, peak_memory = tm.get_traced_memory()
    execution_time = end_time - start_time
    tm.stop()

    print(f"\nMaze #{maze_num} solution:")
    if success:
        maze.print_maze(path, visited)
        print(f"Solution found: {success}")
        print(f"Total nodes visited: {len(visited)}")
        print(f"Path length: {len(path)}")
        print(f"Optimal path length: {optimal_path_length[i]}")
        print(f"Execution time: {execution_time:.4f} seconds")
        print(f"Memory usage: {current_memory/1024:.2f} KB")
    else:
        maze.print_maze(None, visited)
        print(f"Solution found: {success}")
        print(f"Total nodes visited: {len(visited)}")
        print(f"Execution time: {execution_time:.4f} seconds")
        print(f"Memory usage: {current_memory/1024:.2f} KB")