#12*6 connect 4
import numpy as np
from math import inf
from collections import defaultdict

class Minimax:
    def __init__(self, board, player):
        self.update_board(board, player)
        self.configure_dict()

    def configure_dict(self):
        self.moves = defaultdict(int)
        self.playerCount = defaultdict(int)
        self.playerCount['human'] = 0
        self.playerCount['computer'] = 0
        [self.moves[str(k)] for k in range(12)]

    def update_board(self, board, player):
        mask, position, human = '', '', ''
        for j in range(11, -1, -1):
            mask += '0'
            position += '0'
            human += '0'
            #start with the upper row
            for i in range(6):
                mask += ['0', '1'][board[i, j] != 0]
                position += ['0', '1'][board[i, j] == player]
                human += ['0', '1'][board[i, j] == 1]
        self.mask = int(mask, 2)
        self.position = int(position, 2)
        self.human = int(human, 2)

    def connected_four(self):
        #Horizontal check
        check = self.position & (self.position >> 7)
        if check & (check >> 14) : return True

        #Diagonal \
        check = self.position & (self.position)
        if check & (check >> 12) : return True

        #Diagonal /
        check = self.position & (self.position >> 8)
        if check & (check >> 16) : return True

        #Vertical
        check = self.position & (self.position >> 1)
        if check & (check >> 2): return True
        
        #Human check
        #Horizontal check
        check = self.human & (self.human >> 7)
        if check & (check >> 14) : return True

        #Diagonal \
        check = self.human & (self.human)
        if check & (check >> 12) : return True

        #Diagonal /
        check = self.human & (self.human >> 8)
        if check & (check >> 16) : return True

        #Vertical
        check = self.human & (self.human >> 1)
        if check & (check >> 2): return True

        return False
    
    def make_move(self, col, maxPlayer):
        if maxPlayer :
            self.position = self.position ^ self.mask #apply a XOR
            self.mask = self.mask | (self.mask + (1 << (col*7)))
            #return newPosition, newMask
        else :
            self.human = self.human ^ self.mask #apply a XOR
            self.mask = self.mask | (self.mask + (1 << (col*7)))
            #return newPosition, newMask
    
    def undo_move(self, col, maxPlayer):
        if maxPlayer :
            self.mask = self.mask & (self.mask + (1 << (col*7)))
            self.position = self.position ^ self.mask
            #return newPosition, self.self.mask
        else :
            self.mask = self.mask & (self.mask + (1 << (col*7)))
            self.human = self.human ^ self.mask
            #return newPosition, self.self.mask

    def actions(self):
        return [int(column) for column in self.moves if self.moves[column] <= 6]
    
    def utility(self, computer=True):
        return -(37 - self.moves['human']) if computer else (37 - self.moves['computer'])

    def minimax(self, depth, alpha, beta, maxPlayer):
        if depth==0 or self.connected_four():
            score = self.utility(maxPlayer)
            return [-1, score]
        
        if maxPlayer:
            maxScore = [-1, -inf]
            actions = self.actions()
            for action in actions:
                j = action
                self.make_move(j, maxPlayer)
                score = self.minimax(depth-1, alpha, beta, False)
                self.undo_move(j, maxPlayer)
                score[0] = j
                maxScore = maxScore if maxScore[1] >= score[1] else score
                if maxScore[1] >= beta : 
                    return maxScore
                alpha = max(alpha, maxScore[1])
            return maxScore
        else :
            minScore = [-1, +inf]
            actions = self.actions()
            for action in actions:
                j = action
                self.make_move(j, maxPlayer)
                score = self.minimax(depth-1, alpha, beta, True)
                self.undo_move(j, maxPlayer)
                score[0] = j
                minScore = minScore if minScore[1] <= score[1] else score
                if minScore[1] <= alpha : 
                    return minScore
                beta = min(beta, minScore[1])
            return minScore