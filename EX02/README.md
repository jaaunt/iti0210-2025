# EX02 – Monte Carlo Connect Four Solver

## Move Analysis

I chose the following board position as an interesting case:

```
|       |
|       |
|       |
|XOX    |
|OOXOOX |
|XOXXXO |
|0123456|
To move: X
```

### Legal moves

From this position, the legal moves are the columns that are not full:

```
[0, 1, 2, 3, 4, 5, 6]
```

### Simulation results

After running **360 Monte Carlo simulations per move**, the algorithm estimated the following win rates for player `X`:

| Move (Column) | Wins | Draws | Simulations | Win % (approx) |
| ------------- | ---- | ----- | ----------- | -------------- |
| 0             | 135  | 1     | 360         | 37.6%          |
| 1             | 238  | 2     | 360         | 66.4%          |
| 2             | 360  | 0     | 360         | 100.0%         |
| 3             | 171  | 0     | 360         | 47.5%          |
| 4             | 153  | 0     | 360         | 42.5%          |
| 5             | 159  | 0     | 360         | 44.2%          |
| 6             | 143  | 1     | 360         | 39.9%          |

### Algorithm’s Choice

The algorithm chose **column 2** as the best move because it had the highest win rate.

---

## How the Solver Works

* **Legal Moves:** The program first checks which columns are playable (not full at the top row).
* **Monte Carlo Simulation:**
  For each possible move:

  1. Make the move on a copy of the board.
  2. Play random moves until the game ends (random rollout).
  3. Track the outcome: win, loss, or draw.
  4. Repeat this process hundreds of times (360 in this case).
* **Scoring:**
  Win = 1 point, Draw = 0.5 points, Loss = 0 points.
  The move with the highest average score is chosen.
* **Execution:** The chosen move is applied to the real game board and the new state is printed.

---

## Defence Video

Link: https://youtu.be/Dou1z7UNNxM
