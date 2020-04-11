#12*6 connect 4
import numpy as np
from math import inf

class Minimax:
    def __init__(self):
        self.position = 0
        self.mask = 0

    def update_board(self, board, player):
        position, mask = '', ''
        for j in range(11, -1, -1):
            mask += '0'
            position += '0'
            #start with the upper row
            for i in range(6):
                mask += ['0', '1'][board[i, j] != 0]
                position += ['0', '1'][board[i, j] == player]
        self.position, self.mask = int(position, 2), int(mask, 2)

    def connected_four(self, position):
        #Horizontal check
        check = position & (position >> 7)
        if check & (check >> 14) : return True

        #Diagonal \
        check = position & (position)
        if check & (check >> 12) : return True

        #Diagonal /
        check = position & (position >> 8)
        if check & (check >> 16) : return True

        #Vertical
        check = position & (position >> 1)
        if check & (check >> 2): return True

        return False
    
    def make_move(self, position, mask, col):
        newPosition = position ^ mask #apply a XOR
        newMask = mask | (mask + (1 << col*7))
        return newPosition, newMask

    def actions(self):
        pass

if __name__ == "__main__":
    ai = Minimax()