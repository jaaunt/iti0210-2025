# EX01 – Pathfinding and N-Queens

## Overview
This project implements two classic algorithmic problems:

- Pathfinding Solver using BFS, Greedy Best-First Search, and A*.
- N-Queens Solver using backtracking.

The program reads input from stdin and outputs the solution path or board configuration.  
It is implemented in Python.

---

## Part 1 – Pathfinding

### Approach
For the pathfinding task, I implemented three different search algorithms: BFS, Greedy Best-First, and A*.

- **BFS** explores nodes level by level from the start, guaranteeing the shortest path in terms of steps but not considering distance heuristics.
- **Greedy Best-First** expands the node closest to the goal based on the Manhattan distance heuristic. It is faster but does not guarantee the shortest path.
- **A\*** combines the benefits of both by considering both the actual cost from the start and the estimated cost to the goal (`f(n) = g(n) + h(n)`). This makes it generally faster than BFS while still guaranteeing an optimal solution.

All algorithms:
- Use a queue or priority queue to manage the frontier
- Keep track of visited nodes to avoid re-exploration
- Use a parent map to reconstruct the path once the goal is found
- Mark the resulting path with '.' characters on the grid

---

## Part 2 – N-Queens

### Approach
For the N-Queens problem, I used a backtracking algorithm.

The algorithm places queens row by row and recursively tries to place the next queen in a safe column.  
A position is considered safe if:
- No other queen is in the same column
- No other queen is on the same diagonal

If a conflict occurs, the algorithm backtracks and tries the next column. This continues until either:
- All N queens are placed successfully (solution found)
- Or all positions are tried with no valid configuration (no solution)

This guarantees a valid solution when one exists and works efficiently for moderate N (like N = 8).

---

## Benchmarking & Analysis

### Pathfinding
This benchmark measures the average performance of BFS, Greedy Best-First, and A* algorithms on randomly generated maps. 10 iterations for each. With the lava probability set as 20%.

| Algorithm            | Map Size | Time (s) | Nodes Expanded | Path Length |
|-----------------------|----------|----------|----------------|-------------|
| BFS                   | 10x10    |     0.000041s     | NA             | 6.80        |
| Greedy Best-First     | 10x10    |     0.000016s| NA             | 7.20        |
| A*                    | 10x10    |    0.000026s   | NA             | 6.80        |

**Note about node expansion:**  
Ideally, this would also track the number of nodes expanded during the search. However, the original search functions do not provide this information, and modifying them would make the benchmark pointless. 
As it wouldnt be for the same function. Therefore, node expansion counts are not included.

### N-Queens

Example solution for N=8:

Q.......

....Q...

.......Q

.....Q..

..Q.....

......Q.

.Q......

...Q....
