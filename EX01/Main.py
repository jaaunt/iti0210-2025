from collections import deque
import heapq
import sys
from random import randint

# Grid symbols as named constants for clarity and maintainability
START_SYMBOL = 's'
GOAL_SYMBOL = 'D'
LAVA_SYMBOL = '*'
PATH_SYMBOL = '.'

# -----------------------------
# Helper Functions
# -----------------------------

def parse_map(map_lines):
    """
    Convert input lines to a grid and find start and goal coordinates.

    Args:
        map_lines (list[str]): Lines representing the map.

    Returns:
        tuple: (grid as list[list[str]], start (x,y), goal (x,y))
    """
    grid = [list(line) for line in map_lines]
    start = goal = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == START_SYMBOL:
                start = (x, y)
            elif ch == GOAL_SYMBOL:
                goal = (x, y)
    return grid, start, goal


def get_neighbors(pos, grid):
    """
    Return valid neighboring positions (up, left, right, down) that are not lava.

    Args:
        pos (tuple): (x,y) position.
        grid (list[list[str]]): Map grid.

    Returns:
        list[tuple]: Valid neighbor coordinates.
    """
    x, y = pos
    neighbors = []
    # Four possible directions
    for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != LAVA_SYMBOL:
            neighbors.append((nx, ny))
    return neighbors


def reconstruct_path(grid, parent, start, goal):
    """
    Backtrack from goal to start and mark the path on the grid.

    Args:
        grid (list[list[str]]): Map grid to update.
        parent (dict): Node → previous node.
        start (tuple): Start coordinate.
        goal (tuple): Goal coordinate.
    """
    current = goal
    while current != start:
        x, y = current
        if grid[y][x] not in (START_SYMBOL, GOAL_SYMBOL):
            grid[y][x] = PATH_SYMBOL
        current = parent[current]


def manhattan_distance(a, b):
    """Return Manhattan distance between two coordinates."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# -----------------------------
# Pathfinding Algorithms
# -----------------------------

def bfs_search(grid, start, goal):
    """
    Breadth-First Search pathfinding.
    Explores all neighbors level by level until the goal is found.
    """
    frontier = deque([start])  # nodes to visit
    parent = {start: None}     # to reconstruct path

    while frontier:
        current = frontier.popleft()
        if current == goal:
            reconstruct_path(grid, parent, start, goal)
            return

        for neighbor in get_neighbors(current, grid):
            if neighbor not in parent:
                parent[neighbor] = current
                frontier.append(neighbor)


def greedy_best_first_search(grid, start, goal):
    """
    Greedy Best-First Search pathfinding.
    Expands the node closest to the goal (by Manhattan distance).
    """
    frontier = [(manhattan_distance(start, goal), start)]
    parent = {start: None}
    visited = {start}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            reconstruct_path(grid, parent, start, goal)
            return

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                heapq.heappush(frontier, (manhattan_distance(neighbor, goal), neighbor))


def astar_search(grid, start, goal):
    """
    A* pathfinding.
    Expands nodes based on f = g + h (cost so far + estimated distance to goal).
    """
    frontier = [(manhattan_distance(start, goal), 0, start)]  # (f, g, node)
    parent = {start: None}
    g_score = {start: 0}
    visited = set()

    while frontier:
        f, g, current = heapq.heappop(frontier)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            reconstruct_path(grid, parent, start, goal)
            return

        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(frontier, (f_score, tentative_g, neighbor))


def solve_pathfinding(map_data):
    """
    Wrapper for running pathfinding on map input and printing the result.
    """
    grid, start, goal = parse_map(map_data)
    astar_search(grid, start, goal)  # can change to BFS or Greedy if needed
    for row in grid:
        print("".join(row))

# -----------------------------
# N-Queens Solver
# -----------------------------

def clash_pairs(queen_positions):
    """
    Count pairs of queens attacking each other.

    Args:
        queen_positions (list[int]): column positions for each row.

    Returns:
        int: number of attacking pairs.
    """
    n = len(queen_positions)
    total = 0
    for i in range(n):
        for j in range(i+1, n):
            if queen_positions[i] == queen_positions[j] or abs(queen_positions[i] - queen_positions[j]) == j - i:
                total += 1
    return total


def steepest_ascent_nqueens(n, restarts_limit=1000):
    """
    Solve N-Queens using steepest ascent hill climbing with random restarts.
    """
    for _ in range(restarts_limit):
        # Start with random positions for each column
        queen_positions = [randint(0, n-1) for _ in range(n)]
        while True:
            current_cost = clash_pairs(queen_positions)
            if current_cost == 0:
                return queen_positions

            improved = False
            # Try moving each queen to reduce conflicts
            for c in range(n):
                best_row = queen_positions[c]
                best_cost = current_cost
                original_row = queen_positions[c]

                for r in range(n):
                    if r == original_row:
                        continue
                    queen_positions[c] = r
                    cost = clash_pairs(queen_positions)
                    if cost < best_cost:
                        best_cost = cost
                        best_row = r
                        improved = True
                queen_positions[c] = best_row

            if not improved:
                break
    raise ValueError("Failed to find solution after random restarts")


def emit_nqueens_solution(n):
    """
    Print an ASCII board showing an N-Queens solution.
    """
    solution = steepest_ascent_nqueens(n)
    for r in range(n):
        row = ['.'] * n
        for c in range(n):
            if solution[c] == r:
                row[c] = 'Q'
        print("".join(row))


if __name__ == "__main__":
    first_line = sys.stdin.readline()
    if not first_line:
        sys.exit(0)

    value = int(first_line.strip())
    if value < 0:
        emit_nqueens_solution(-value)
    else:
        height = value
        map_rows = [sys.stdin.readline().rstrip("\n") for _ in range(height)]
        solve_pathfinding(map_rows)
