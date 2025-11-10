class Maze:
    """
    Each index representing:
    0: Wall
    1: Path
    -1: Start position
    10: End position
    """
    def __init__(self, maze_number=1):
        self.width = 21
        self.height = 21

        from maze_layouts import get_maze
        self.maze = get_maze(maze_number)

        self.start_pos = self.find_position(-1)
        self.end_pos = self.find_position(10)

    def find_position(self, value):
        # Return the position for START and END position with data structure tuple.
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == value:
                    return (y, x)
        return None

    def print_maze(self, path=None, visited=None):
        # Used for printing current maze state before and after implementation.
        for y in range(self.height):
            for x in range(self.width):
                pos = (y, x)
                if self.maze[y][x] == -1:
                    print("🟥", end="")  # Start
                elif self.maze[y][x] == 10:
                    print("🟩", end="")  # End
                elif path and pos in path:
                    print("🟨", end="")  # Solution path
                elif visited and pos in visited:
                    print("🟪", end="")  # Visited nodes
                elif self.maze[y][x] == 1:
                    print("⬛", end="")  # Path
                else:
                    print("⬜", end="")  # Wall
            print()