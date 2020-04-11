import numpy as np
from Minimax import *

def init_board():
	return np.zeros((6, 12))

if __name__ == "__main__":
	board = init_board()
	board[1,1] = 1
	ai = Minimax()
	a, b = ai.update_board(board, 1)
	print(board)
	print(a)
	print(b)