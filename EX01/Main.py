from Generator import generate_map
import sys

from collections import deque
import heapq


# helper functions

def parse_map(map_lines):
    """
    Converts input to a list and finds start 's' and goal 'D' positions.
    """
    grid = [list(line) for line in map_lines]  # convert each row into a list of characters
    start = goal = None
    for y, row in enumerate(grid):  # loop through rows with index y
        for x, ch in enumerate(row):  # loop through columns with index x
            if ch == 's':  # start
                start = (x, y)
            elif ch == 'D':  # goal
                goal = (x, y)
    return grid, start, goal  # return grid and coordinates of start and goal


def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # left, right, up, down
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != '*':
                neighbors.append((nx, ny))
    return neighbors



def reconstruct_path(grid, parent, start, goal):
    """
    Backtracks from goal to start using the parent dictionary and marks path with '.'.
    """
    current = goal
    while current != start:  # until we reach the start
        x, y = current
        if grid[y][x] not in ('s', 'D'):  # dont overwrite start or goal
            grid[y][x] = '.'  # mark the path
        current = parent[current]  # move to previous node along the path


def manhattan_distance(a, b):
    """
    Computes Manhattan distance between two positions (x1,y1) and (x2,y2).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs_search(grid, start, goal):
    """
    BFS Search.
    """
    queue = deque([start])  # queue for BFS, start with the starting node
    parent = {start: None}  # track parent of each node to reconstruct path

    while queue:  # while there are nodes to explore
        current = queue.popleft()  # get the next node from the front of the queue
        if current == goal:  # if we've reached the goal
            reconstruct_path(grid, parent, start, goal)  # mark path on grid
            return  # finished
        for neighbor in get_neighbors(current, grid):  # explore neighbors
            if neighbor not in parent:  # only visit unvisited neighbors
                parent[neighbor] = current  # track how we got here
                queue.append(neighbor)  # add neighbor to the queue


def greedy_best_first_search(grid, start, goal):
    """
    Greedy Best First Search.
    """
    heap = [(manhattan_distance(start, goal), start)]  # priority queue by: heuristic(manhattan), node
    parent = {start: None}  # track parent nodes
    visited = set([start])  # track visited nodes to avoid revisiting

    while heap:  # while there are nodes in the priority queue
        _, current = heapq.heappop(heap)  # pop node with lowest heuristic
        if current == goal:  # goal reached
            reconstruct_path(grid, parent, start, goal)  # mark path
            return
        for neighbor in get_neighbors(current, grid):  # check neighbors
            if neighbor not in visited:  # only unvisited neighbors
                visited.add(neighbor)  # mark as visited
                parent[neighbor] = current  # track parent
                heapq.heappush(heap, (manhattan_distance(neighbor, goal), neighbor))  # add neighbor to heap


def astar_search(grid, start, goal):
    """
    A* Search.
    """
    heap = [(manhattan_distance(start, goal), 0, start)]  # (f-score = g+h, h-score = heuristic, node coordinates)
    parent = {start: None}  # track parent nodes for path reconstruction
    g_score = {start: 0}  # cost from start to node
    visited = set()  # track nodes already processed to avoid revisiting

    while heap:  # while there are nodes to explore
        f, h, current = heapq.heappop(heap)  # pop node with lowest f-score
        if current in visited:  # skip if already processed
            continue
        visited.add(current)  # mark current node as visited

        if current == goal:  # goal reached
            reconstruct_path(grid, parent, start, goal)  # mark path on grid
            return

        for neighbor in get_neighbors(current, grid):  # explore valid neighbors
            tentative_g = g_score[current] + 1  # cost to reach neighbor from start
            # if neighbor not visited or we found a cheaper path
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g  # update cost to reach neighbor
                f_score = tentative_g + manhattan_distance(neighbor, goal)  # total estimated cost f = g + h
                parent[neighbor] = current  # track parent for path reconstruction
                h_score = manhattan_distance(neighbor, goal)  # heuristic for tie-breaking
                heapq.heappush(heap, (f_score, h_score, neighbor))  # add neighbor to heap

def solve_pathfinding(map_data):
    """
    Which algorithm to run.
    """
    grid, start, goal = parse_map(map_data)  # convert input lines to grid and find start/goal

    # bfs_search(grid, start, goal)  # BFS
    # greedy_best_first_search(grid, start, goal)  # Greedy Best-First
    astar_search(grid, start, goal)  # A*

    for row in grid:  # print the final grid
        print("".join(row))  # join each row back into a string and print


def solve_nqueens(n):
    pass


if __name__ == "__main__":

    # gen test file
    generated = generate_map(10, 10, 0.2)
    lines = generated.splitlines()
    first_line = lines[0]
    rest_lines = lines[1:]

    value = int(first_line)
    if value < 0:
        n = -value
        solve_nqueens(n)
    else:
        map_data = rest_lines
        solve_pathfinding(map_data)
