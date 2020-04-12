#12*6 connect 4
import numpy as np
from math import inf
from collections import defaultdict

class Minimax:
    def __init__(self):
        self.position = ''
        self.mask = ''
        self.human = ''
        self.configure_dict()

    def configure_dict(self):
        self.moves = defaultdict(int)
        self.moves['human'] = 0
        self.moves['computer'] = 0
        [self.moves[str(k)] for k in range(12)]

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
    
    def undo_move(self, position, mask, col):
        newMask = mask & (mask + (1 << (col*7)))
        newPosition = position ^ mask
        return newPosition, newMask
    
    def utility(self, computer=True):
        return 22 - self.moves['computer'] if computer else -(22 - self.moves['human'])

    def minimax(self, depth, alpha, beta, maxPlayer):
        if depth==0 or self.terminal_test():
            score = self.utility()
            return [-1, -1, score]
        
        if maxPlayer:
            maxScore = [-1, -1, -inf]
            actions = self.actions()
            for action in actions:
                i, j = action[0], action[1]
                self.state[i][j] = "O"
                score = self.minimax(depth-1, alpha, beta, False)
                self.state[i][j] = "."
                score[0], score[1] = i, j
                maxScore = maxScore if maxScore[2] >= score[2] else score
                if maxScore[2] >= beta : 
                    return maxScore
                alpha = max(alpha, maxScore[2])
            return maxScore
        else :
            minScore = [-1, -1, +inf]
            actions = self.actions()
            for action in actions:
                i, j = action[0], action[1]
                self.state[i][j] = "X"
                score = self.minimax(depth-1, alpha, beta, True)
                self.state[i][j] = "."
                score[0], score[1] = i, j
                minScore = minScore if minScore[2] <= score[2] else score
                if minScore[2] <= alpha : 
                    return minScore
                beta = min(beta, minScore[2])
            return minScore

if __name__ == "__main__":
    ai = Minimax()
    print(ai.moves)