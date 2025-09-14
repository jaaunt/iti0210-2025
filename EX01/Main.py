from collections import deque
import heapq
import sys
from random import randint

# helper functions

def parse_map(map_lines):
    """Convert input to a grid and find start 's' and goal 'D' coordinates."""
    grid = [list(line) for line in map_lines]  # convert each row into a list
    start = goal = None
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == 's':
                start = (x, y)
            elif ch == 'D':
                goal = (x, y)
    return grid, start, goal

def get_neighbors(pos, grid):
    """Return valid neighboring positions (up, left, right, down) that are not lava '*'."""
    x, y = pos
    neighbors = []
    for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:  # up, left, right, down
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != '*':
            neighbors.append((nx, ny))
    return neighbors

def reconstruct_path(grid, parent, start, goal):
    """Backtrack from goal to start and mark path with '.'."""
    current = goal
    while current != start:
        x, y = current
        if grid[y][x] not in ('s', 'D'):
            grid[y][x] = '.'
        current = parent[current]

def manhattan_distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# BFS

def bfs_search(grid, start, goal):
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            reconstruct_path(grid, parent, start, goal)
            return
        for neighbor in get_neighbors(current, grid):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)

# Greedy Best-First

def greedy_best_first_search(grid, start, goal):
    heap = [(manhattan_distance(start, goal), start)]
    parent = {start: None}
    visited = {start}
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            reconstruct_path(grid, parent, start, goal)
            return
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                heapq.heappush(heap, (manhattan_distance(neighbor, goal), neighbor))

# A*

def astar_search(grid, start, goal):
    heap = [(manhattan_distance(start, goal), 0, start)]  # f, g, current
    parent = {start: None}
    g_score = {start: 0}
    visited = set()
    while heap:
        f, g, current = heapq.heappop(heap)
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
                heapq.heappush(heap, (f_score, tentative_g, neighbor))

# solve pathfinding

def solve_pathfinding(map_data):
    grid, start, goal = parse_map(map_data)
    astar_search(grid, start, goal)
    for row in grid:
        print("".join(row))

# N-Queens

def clash_pairs(cols):
    """Count pairs of queens in conflict."""
    N = len(cols)
    total = 0
    for i in range(N):
        for j in range(i+1, N):
            if cols[i] == cols[j] or abs(cols[i]-cols[j]) == j-i:
                total += 1
    return total

def steepest_ascent_nqueens(N, restarts_limit=1000):
    """Solve N-Queens using steepest ascent + random restarts."""
    for _ in range(restarts_limit):
        cols = [randint(0, N-1) for _ in range(N)]
        while True:
            cur_cost = clash_pairs(cols)
            if cur_cost == 0:
                return cols
            moved = False
            for c in range(N):
                best_row = cols[c]
                best_cost = cur_cost
                orig_row = cols[c]
                for r in range(N):
                    if r == orig_row:
                        continue
                    cols[c] = r
                    cost = clash_pairs(cols)
                    if cost < best_cost:
                        best_cost = cost
                        best_row = r
                        moved = True
                cols[c] = best_row
            if not moved:
                break
    raise ValueError("Failed to find solution after random restarts")

def emit_nqueens_solution(N):
    cols = steepest_ascent_nqueens(N)
    for r in range(N):
        row = ['.']*N
        for c in range(N):
            if cols[c] == r:
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
        H = value
        map_rows = [sys.stdin.readline().rstrip("\n") for _ in range(H)]
        solve_pathfinding(map_rows)
