import random  # for random moves
import copy  # to save copies of the boards
import sys  # to read input

ROWS = 6
COLS = 7  # board measurements
WIN_LENGTH = 4  # how many in a row to win
SIMULATIONS_PER_MOVE = 360  # bigger num more accurate smaller num faster
# random rollout amount per move

def get_legal_moves(board):
    """Find all non-full columns."""
    # from the first row if theres an emmmpty spot on top of that row u its playable
    return [c for c in range(COLS) if board[0][c] == " "]

def make_move(board, column, player):
    """Places a player's token in a column, modifies the board in-place."""
    for r in range(ROWS - 1, -1, -1):
        # go up one row each time
        # check from bottom to top
        if board[r][column] == " ":
            # check if empty
            board[r][column] = player  # put either O or X there
            return True
    return False

def check_winner(board):
    """Return 'X' or 'O' if someone won, 'D' if draw, else None."""
    # check horizontal, vertical, and both diagonals
    # the win conditions
    # 4 in a row either vertically, horisontally or diagonally
    for r in range(ROWS):  # check every row
        for c in range(COLS):  # every column
            if board[r][c] == " ":  # if empty no point in checking
                continue
            player = board[r][c]  # remember the player if its the x or o one
            # player depends on whats in the place we are checking right now

            # horizontal
            # last c where a win is possible is 3 since 3,4,5,6(7-4=3=3) if its 4 4,5,6 (4>7-4=3)
            if c <= COLS - WIN_LENGTH and all(board[r][c+i] == player for i in range(WIN_LENGTH)):
                # all must be the players type
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

    # check for draw
    # if no one won earlier and the board is full
    # its a draw
    if all(board[0][c] != " " for c in range(COLS)):
        return "D"

    return None

def random_rollout(board, player):
    """Play random moves until game ends. Return winner ('X','O','D')."""
    current = player
    while True:
        winner = check_winner(board)  # check if someone won
        if winner:
            return winner  # if someone won return it
        legal = get_legal_moves(board)  # get places you can acc choose
        if not legal:
            return "D"  # if no legal moves left and no one won before draw
        move = random.choice(legal)  # choose randomly from legal moves
        make_move(board, move, current)  # make the move
        current = "O" if current == "X" else "X"  # change to other players turn

def solve_monte_carlo(board_state, player_to_move):
    """
    Decide and execute the best move for the current player using pure Monte Carlo simulation.

    Steps:
    1. Get all legal moves.
    2. For each legal move:
        - Simulate the move on a copy of the board.
        - Play out the rest of the game with random moves (rollouts) until the game ends.
        - Record whether the initial move led to a win, loss, or draw for the current player.
    3. Estimate the win rate of each move as:
           win_rate = (wins + 0.5 * draws) / simulations
    4. Select the move with the highest win rate.
    5. Apply the chosen move to the real board and print the updated state.
    """
    legal_moves = get_legal_moves(board_state)  # all legal moves
    move_wins = {m: 0 for m in legal_moves}  # how many times it leads to a win or draw
    move_sims = {m: 0 for m in legal_moves}  # how many simulations for that move

    for move in legal_moves:  # for every move try it up to the sim max amount
        for _ in range(SIMULATIONS_PER_MOVE):
            sim_board = copy.deepcopy(board_state)  # make a copy of the game so you dont fuck up the real one
            make_move(sim_board, move, player_to_move)  # make the move
            winner = random_rollout(sim_board, "O" if player_to_move == "X" else "X")
            # play to the end with random moves get who wins or if its a draw
            move_sims[move] += 1  # count the simulations
            if winner == player_to_move:  # if the player whos moving wins add 1
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
