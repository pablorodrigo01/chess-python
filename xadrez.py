import tkinter as tk
import chess

# Criação da janela principal
root = tk.Tk()
root.title("Jogo de Xadrez")

# Criação do tabuleiro
board_frame = tk.Frame(root)
board_frame.pack()

# Lista com as peças do xadrez (representadas por caracteres Unicode)
piece_symbols = {
    chess.PAWN: '♟',
    chess.KNIGHT: '♞',
    chess.BISHOP: '♝',
    chess.ROOK: '♜',
    chess.QUEEN: '♛',
    chess.KING: '♚'
}

# Dicionário com as cores das peças
piece_colors = {
    chess.WHITE: "white",
    chess.BLACK: "black"
}

# Dicionário com as cores do tabuleiro
board_colors = {}
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            board_colors[(row, col)] = "#B58863"
        else:
            board_colors[(row, col)] = "#F0D9B5"


# Instância do objeto do tabuleiro de xadrez
board = chess.Board()

# Função para criar as casas do tabuleiro
def create_square(row, col, piece=None):
    square = tk.Frame(board_frame, width=60, height=60, bg=board_colors[(row, col)], highlightthickness=0)
    square.grid(row=row+1, column=col+1)

    if piece is not None:
        square = tk.Frame(board_frame, width=60, height=60, bg=board_colors[(row, col)], highlightthickness=0)
        square.grid(row=row+1, column=col+1)

        label = tk.Label(square, text=piece_symbols[piece.piece_type], font=("Arial", 32), fg=piece_colors[piece.color], bg=board_colors[(row, col)])
        label.pack(fill='both')

# Função para atualizar o tabuleiro
def update_board():
    for row in range(8):
        for col in range(8):
            square = board.piece_at(chess.square(col, 7 - row))
            create_square(row, col, square)

# Função para processar o movimento inserido
def process_move():
    move = move_entry.get()
    try:
        move = board.parse_san(move)
        if move in board.legal_moves:
            board.push(move)
            update_board()
            check_game_status()
            show_possible_moves()
        else:
            print("Movimento inválido. Tente novamente.")
    except ValueError:
        print("Movimento inválido. Tente novamente.")

# Função para verificar o estado do jogo
def check_game_status():
    if board.is_checkmate():
        print("Xeque-mate!")
    elif board.is_stalemate():
        print("Empate por afogamento!")
    elif board.is_insufficient_material():
        print("Empate por material insuficiente!")
    elif board.is_seventyfive_moves():
        print("Empate por regra das 75 jogadas!")
    elif board.is_fivefold_repetition():
        print("Empate por repetição de posição!")

# Função para mostrar os movimentos possíveis
def show_possible_moves():
    possible_moves = [move.uci() for move in board.legal_moves]
    moves_text = "Movimentos possíveis:\n"
    max_chars_per_line = 30
    line_length = 0

    for move in possible_moves:
        move_text = board.san(chess.Move.from_uci(move))
        if line_length + len(move_text) + 2 > max_chars_per_line:
            moves_text += "\n"
            line_length = 0

        moves_text += move_text + ", "
        line_length += len(move_text) + 2

    moves_label.config(text=moves_text)

# Criação dos números e letras nos cantos do tabuleiro
for i in range(8):
    tk.Label(board_frame, text=chr(97 + i), font=("Arial", 14)).grid(row=0, column=i+1)
    tk.Label(board_frame, text=str(8-i), font=("Arial", 14)).grid(row=i+1, column=0)

# Criação do campo de entrada para o movimento
move_entry = tk.Entry(root, font=("Arial", 14))
move_entry.pack(pady=10)

# Criação do botão para processar o movimento
move_button = tk.Button(root, text="Mover", font=("Arial", 14), command=process_move)
move_button.pack(pady=5)

# Criação do rótulo para mostrar os movimentos possíveis
moves_label = tk.Label(root, text="Movimentos possíveis:", font=("Arial", 14))
moves_label.pack(pady=10)

# Criação do rótulo para exibir os movimentos possíveis
possible_moves_label = tk.Label(root, text="", font=("Arial", 14))
possible_moves_label.pack()

# Inicialização do tabuleiro
update_board()
show_possible_moves()

# Execução da interface gráfica
root.mainloop()
