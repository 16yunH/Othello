import time
import sys
import random

# board, piece, and stone constants
BLACK, WHITE, EMPTY = -1, 1, 0

if "idlelib" in sys.modules:
    BLACK_PIECE = " ● "
    WHITE_PIECE = " ○ "
    EMPTY_PIECE = " □ "
    END_ROW = " "
else:
    BG_EMPTY, BG_RESET = "\x1b[42m", "\x1b[0m"
    BLACK_PIECE = f"{BG_EMPTY}⚫️{BG_RESET}"
    EMPTY_PIECE = f"{BG_EMPTY}🟩{BG_RESET}"
    WHITE_PIECE = f"{BG_EMPTY}⚪️{BG_RESET}"
    END_ROW = f"{BG_EMPTY} {BG_RESET}"

def stone(piece):
    stone_coes = [
        BLACK_PIECE,
        EMPTY_PIECE,
        WHITE_PIECE,
    ]
    return stone_coes[piece + 1]

def init_board(n=8):
    board = [[0 for _ in range(n)] for _ in range(n)]
    C0, C1 = n // 2, n // 2 - 1
    board[C0][C0], board[C1][C1] = WHITE, WHITE  # White
    board[C1][C0], board[C0][C1] = BLACK, BLACK  # Black
    return board

def display_board(board, sleep=0):
    size = len(board)
    print("   ", end="")
    for col in range(size):
        print(chr(ord("A") + col), end=" ")
    print()
    for i, row in enumerate(board):
        print(chr(ord("A") + i), end=" ")
        for piece in row:
            print(stone(piece), end="")
        print(END_ROW, end="")
        print()  # New line after each row
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    print(f"⚫️ {black_count}      ⚪️ {white_count}")
    if sleep > 0:
        time.sleep(sleep)
        
def is_valid_move(board, row, col, piece):
    if board[row][col] != EMPTY:
        return False
    valid = False
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        has_opponent_piece = False
        while 0 <= r < len(board) and 0 <= c < len(board):
            if board[r][c] == -piece:
                has_opponent_piece = True
            elif board[r][c] == piece:
                if has_opponent_piece:
                    valid = True
                break
            else:
                break
            r += dr
            c += dc
    return valid

def get_valid_moves(board, piece):
    n = len(board)
    moves = []
    for row in range(n):
        for col in range(n):
            if is_valid_move(board, row, col, piece):
                moves.append((row, col))
    return moves

def move_input(board, piece, name):
    if not get_valid_moves(board, piece):
        return None, None
    while True:
        print(f"{name}, enter your move (row col) or '?' for valid moves:")
        try:
            user_input = input().split()
            if user_input[0] == '?':
                valid_moves = get_valid_moves(board, piece)
                print("Valid moves:")
                best_move = None
                best_eval = float('-inf')
                for valid_move in valid_moves:
                    board[valid_move[0]][valid_move[1]] = piece
                    eval, _ = minimax(board, 3, False, float('-inf'), float('inf'), piece)
                    board[valid_move[0]][valid_move[1]] = EMPTY
                    if eval > best_eval:
                        best_eval = eval
                        best_move = valid_move
                for mv in valid_moves:
                    if mv == best_move:
                        print(f"{chr(ord('A') + mv[0])} {chr(ord('A') + mv[1])}   recommended")
                    else:
                        print(f"{chr(ord('A') + mv[0])} {chr(ord('A') + mv[1])}")
                continue
            row, col = ord(user_input[0]) - ord('A'), ord(user_input[1]) - ord('A')
            if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == EMPTY and is_valid_move(board, row, col, piece):
                return row, col
            else:
                print("Invalid move, try again.")
        except (ValueError, IndexError):
            print("Invalid input, try again.")

def move_random(board, piece, name):
    moves = get_valid_moves(board, piece)
    return random.choice(moves) if moves else (None, None)

def evaluate_board(board, piece):
    score = 0
    for row in board:
        for cell in row:
            if cell == piece:
                score += 1
            elif cell == -piece:
                score -= 1
    return score

def minimax(board, depth, is_maximizing, alpha, beta, piece):
    if depth == 0 or check_finished(board):
        return evaluate_board(board, piece), None
    if is_maximizing:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, piece):
            board[move[0]][move[1]] = piece
            eval, _ = minimax(board, depth - 1, False, alpha, beta, piece)
            board[move[0]][move[1]] = EMPTY
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_valid_moves(board, -piece):
            board[move[0]][move[1]] = -piece
            eval, _ = minimax(board, depth - 1, True, alpha, beta, piece)
            board[move[0]][move[1]] = EMPTY
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def move_AI(board, piece, name):
    best_move = None
    best_eval = float('-inf')
    for move in get_valid_moves(board, piece):
        board[move[0]][move[1]] = piece
        eval, _ = minimax(board, 3, False, float('-inf'), float('inf'), piece)
        board[move[0]][move[1]] = EMPTY
        if eval > best_eval:
            best_eval = eval
            best_move = move
    if best_move:
        print(f"{name} moves to {chr(ord('A') + best_move[0])} {chr(ord('A') + best_move[1])}")
    return best_move if best_move else (None, None)

def move_AI_random(board, piece, name):
    moves = move_random(board, piece, name)
    if moves[0] is not None and moves[1] is not None:
        print(f"{name} moves to {chr(ord('A') + moves[0])} {chr(ord('A') + moves[1])}")
    return moves

def get_opposite_piece(piece):
    return -piece

def flip_pieces(board, row, col, piece):
    opposite_piece = get_opposite_piece(piece)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_piece:
            r, c = r + dr, c + dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == piece:
            r, c = row + dr, col + dc
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_piece:
                board[r][c] = piece
                r, c = r + dr, c + dc
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_piece:
            r, c = r - dr, c - dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == piece:
            r, c = row - dr, col - dc
            while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_piece:
                board[r][c] = piece
                r, c = r - dr, c - dc
            
def do_move(board, row, col, piece):
    board[row][col] = piece
    flip_pieces(board, row, col, piece)

def move_one_step(player, board):
    name, piece, move = player['name'], player['piece'], player['move']
    row, col = move(board, piece, name)
    if row is None or col is None:
        return False
    if not is_valid_move(board, row, col, piece):
        return False
    do_move(board, row, col, piece)
    display_board(board)
    return True
    
def check_finished(board):
    return len(get_valid_moves(board, BLACK)) == 0 and len(get_valid_moves(board, WHITE)) == 0

def game(player1, player2, n=8):
    board = init_board(n)
    player1['piece'], player2['piece'] = BLACK, WHITE
    display_board(board)
    current_player = player1
    while True:
        if check_finished(board):
            break
        if not move_one_step(current_player, board):
            print(f"{current_player['name']} has no valid moves and passes.")
        current_player = player2 if current_player == player1 else player1
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    if black_count > white_count:
        print(f"{player1['name']} wins!")
    elif white_count > black_count:
        print(f"{player2['name']} wins!")
    else:
        print("It's a tie!")

def create_player(name, move):
    return {
        "name": name,
        "move": move,
        "piece": None,
    }

def test_board():
    board = init_board()
    display_board(board)

if __name__ == "__main__":
    test_board()
