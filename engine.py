import random

def make_move(board, move):
    r1, c1, r2, c2 = move
    new = [row[:] for row in board]
    piece = new[r1][c1]
    new[r2][c2] = piece
    new[r1][c1] = ""
    if piece == "wp" and r2 == 0: new[r2][c2] = "wq"
    if piece == "bp" and r2 == 7: new[r2][c2] = "bq"
    if piece[1] == "k" and abs(c2 - c1) == 2:
        if c2 == 6:
            new[r2][5], new[r2][7] = new[r2][7], ""
        elif c2 == 2:
            new[r2][3], new[r2][0] = new[r2][0], ""
    if piece[1] == "p" and abs(c2 - c1) == 1 and board[r2][c2] == "":
        new[r1][c2] = ""
    return new

def get_moves(board, color, move_log=[], check_castling=True):
    moves = []
    for r in range(8):
        for c in range(8):
            if board[r][c] != "" and board[r][c][0] == color:
                p = board[r][c][1]
                if p == "p":
                    d = -1 if color == "w" else 1
                    if 0 <= r + d < 8 and board[r + d][c] == "":
                        moves.append((r, c, r + d, c))
                        if ((color == "w" and r == 6) or (color == "b" and r == 1)) and board[r+d][c] == "" and board[r+2*d][c] == "":
                            moves.append((r, c, r + 2 * d, c))
                    for dc in [-1, 1]:
                        if 0 <= c + dc < 8 and 0 <= r + d < 8:
                            if board[r + d][c + dc] != "" and board[r + d][c + dc][0] != color:
                                moves.append((r, c, r + d, c + dc))
                            if len(move_log) > 0:
                                last_m, last_p = move_log[-1]
                                if last_p[1] == "p" and abs(last_m[2]-last_m[0]) == 2 and last_m[2] == r and last_m[3] == c + dc:
                                    moves.append((r, c, r + d, c + dc))
                elif p == "n":
                    for dr, dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            if board[nr][nc] == "" or board[nr][nc][0] != color:
                                moves.append((r, c, nr, nc))
                elif p in ["r", "b", "q"]:
                    dirs = []
                    if p in ["r", "q"]: dirs += [(1,0),(-1,0),(0,1),(0,-1)]
                    if p in ["b", "q"]: dirs += [(1,1),(1,-1),(-1,1),(-1,-1)]
                    for dr, dc in dirs:
                        for i in range(1, 8):
                            nr, nc = r+dr*i, c+dc*i
                            if 0<=nr<8 and 0<=nc<8:
                                if board[nr][nc] == "": moves.append((r,c,nr,nc))
                                elif board[nr][nc][0] != color:
                                    moves.append((r,c,nr,nc))
                                    break
                                else: break
                            else: break
                elif p == "k":
                    for dr in [-1,0,1]:
                        for dc in [-1,0,1]:
                            if dr==0 and dc==0: continue
                            nr, nc = r+dr, c+dc
                            if 0<=nr<8 and 0<=nc<8:
                                if board[nr][nc] == "" or board[nr][nc][0] != color:
                                    moves.append((r,c,nr,nc))
                    if check_castling and not is_in_check(board, color, move_log):
                        if can_castle(board, color, move_log, "king"): moves.append((r, c, r, 6))
                        if can_castle(board, color, move_log, "queen"): moves.append((r, c, r, 2))
    return moves

def can_castle(board, color, move_log, side):
    r = 7 if color == "w" else 0
    if any(p == color + "k" for _, p in move_log): return False
    opp = "b" if color == "w" else "w"
    if side == "king":
        if any(p == color + "r" and m[1] == 7 for m, p in move_log): return False
        if board[r][5] == "" and board[r][6] == "" and board[r][7] == color + "r":
            return not is_attacked(board, r, 5, opp, move_log) and not is_attacked(board, r, 6, opp, move_log)
    else:
        if any(p == color + "r" and m[1] == 0 for m, p in move_log): return False
        if board[r][1] == "" and board[r][2] == "" and board[r][3] == "" and board[r][0] == color + "r":
            return not is_attacked(board, r, 2, opp, move_log) and not is_attacked(board, r, 3, opp, move_log)
    return False

def is_attacked(board, r, c, opp_color, move_log):
    opp_moves = get_moves(board, opp_color, move_log, False)
    return any(m[2] == r and m[3] == c for m in opp_moves)

def is_in_check(board, color, move_log=[]):
    k = color + "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == k: return is_attacked(board, r, c, "b" if color=="w" else "w", move_log)
    return False

def get_valid_moves(board, color, move_log=[]):
    moves = get_moves(board, color, move_log)
    return [m for m in moves if not is_in_check(make_move(board, m), color, move_log)]

def is_checkmate(board, color, move_log=[]):
    return is_in_check(board, color, move_log) and len(get_valid_moves(board, color, move_log)) == 0

def is_stalemate(board, color, move_log=[]):
    return not is_in_check(board, color, move_log) and len(get_valid_moves(board, color, move_log)) == 0

def random_ai(board, color, move_log=[]):
    valid = get_valid_moves(board, color, move_log)
    if not valid: return None
    caps = [m for m in valid if board[m[2]][m[3]] != ""]
    return random.choice(caps) if caps else random.choice(valid)

# Hàm đánh giá bàn cờ đơn giản
def evaluate_board(board):
    piece_values = {
        'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 0
    }
    value = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece:
                sign = 1 if piece[0] == 'w' else -1
                value += sign * piece_values.get(piece[1], 0)
    return value

# Minimax với cắt tỉa alpha-beta
def minimax(board, color, move_log, depth, alpha, beta, maximizing):
    if depth == 0 or is_checkmate(board, color, move_log) or is_stalemate(board, color, move_log):
        return evaluate_board(board), None
    valid_moves = get_valid_moves(board, color, move_log)
    if not valid_moves:
        return evaluate_board(board), None
    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in valid_moves:
            new_board = make_move(board, move)
            new_log = move_log + [(move, board[move[0]][move[1]])]
            eval, _ = minimax(new_board, 'b' if color == 'w' else 'w', new_log, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in valid_moves:
            new_board = make_move(board, move)
            new_log = move_log + [(move, board[move[0]][move[1]])]
            eval, _ = minimax(new_board, 'b' if color == 'w' else 'w', new_log, depth-1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

# AI sử dụng minimax
def minimax_ai(board, color, move_log=[], depth=2):
    _score, move = minimax(board, color, move_log, depth, float('-inf'), float('inf'), True)
    return move

# Kết hợp: chọn N nước đi tốt nhất theo minimax, rồi random trong số đó
def ai_hybrid(board, color, move_log=[], depth=2, top_n=3):
    valid_moves = get_valid_moves(board, color, move_log)
    if not valid_moves:
        return None
    scored_moves = []
    for move in valid_moves:
        new_board = make_move(board, move)
        new_log = move_log + [(move, board[move[0]][move[1]])]
        score, _ = minimax(new_board, 'b' if color == 'w' else 'w', new_log, depth-1, float('-inf'), float('inf'), False)
        scored_moves.append((score, move))
    # Sắp xếp theo điểm số (AI là màu đen nên chọn min nếu là đen, max nếu là trắng)
    reverse = color == 'w'
    scored_moves.sort(reverse=reverse)
    top_moves = [m for _, m in scored_moves[:top_n]]
    return random.choice(top_moves)