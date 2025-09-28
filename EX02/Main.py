import random
import copy
import sys

ROWS = 6
COLS = 7
WIN_LENGTH = 4
SIMULATIONS_PER_MOVE = 400  # bigger num more accurate smaller num faster

def get_legal_moves(board):
    """Find all non-full columns."""
    return [c for c in range(COLS) if board[0][c] == " "]

def make_move(board, column, player):
    """Places a player's token in a column, modifies the board in-place."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][column] == " ":
            board[r][column] = player
            return True
    return False

def check_winner(board):
    """Return 'X' or 'O' if someone won, 'D' if draw, else None."""
    # check horizontal, vertical, and both diagonals
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                continue
            player = board[r][c]

            # horizontal
            if c <= COLS - WIN_LENGTH and all(board[r][c+i] == player for i in range(WIN_LENGTH)):
                return player
            # vertical
            if r <= ROWS - WIN_LENGTH and all(board[r+i][c] == player for i in range(WIN_LENGTH)):
                return player
            # diag down-right
            if r <= ROWS - WIN_LENGTH and c <= COLS - WIN_LENGTH and all(board[r+i][c+i] == player for i in range(WIN_LENGTH)):
                return player
            # diag up-right
            if r >= WIN_LENGTH - 1 and c <= COLS - WIN_LENGTH and all(board[r-i][c+i] == player for i in range(WIN_LENGTH)):
                return player

    # check draw
    if all(board[0][c] != " " for c in range(COLS)):
        return "D"

    return None

def random_rollout(board, player):
    """Play random moves until game ends. Return winner ('X','O','D')."""
    current = player
    while True:
        winner = check_winner(board)
        if winner:
            return winner
        legal = get_legal_moves(board)
        if not legal:
            return "D"
        move = random.choice(legal)
        make_move(board, move, current)
        current = "O" if current == "X" else "X"

def solve_monte_carlo(board_state, player_to_move):
    legal_moves = get_legal_moves(board_state)
    move_wins = {m: 0 for m in legal_moves}
    move_sims = {m: 0 for m in legal_moves}

    for move in legal_moves:
        for _ in range(SIMULATIONS_PER_MOVE):
            sim_board = copy.deepcopy(board_state)
            make_move(sim_board, move, player_to_move)
            winner = random_rollout(sim_board, "O" if player_to_move == "X" else "X")
            move_sims[move] += 1
            if winner == player_to_move:
                move_wins[move] += 1
            elif winner == "D":
                move_wins[move] += 0.5  # half points for draw

    # choose the best move
    best_move = max(legal_moves, key=lambda m: move_wins[m] / move_sims[m])

    # acc move on the board
    make_move(board_state, best_move, player_to_move)

    # print the board state
    for row in board_state:
        print("|" + "".join(row) + "|")
    print("|0123456|")
    next_player = "O" if player_to_move == "X" else "X"
    print(f"To move: {next_player}")
    print("Your move?")

if __name__ == "__main__":
    lines = [sys.stdin.readline().rstrip("\n") for _ in range(9)]
    board = [list(line[1:-1]) for line in lines[0:6]]
    player = lines[7].split(": ")[1]
    solve_monte_carlo(board, player)
