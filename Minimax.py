#12*6 connect 4
from copy import deepcopy
from math import inf
from collections import defaultdict

class Minimax:
    def __init__(self, board, player):
        self.configure_dict()
        self.update_board(board, player)

    def configure_dict(self):
        self.moves = defaultdict(int)
        self.playerCount = defaultdict(int)
        [self.moves[str(k)] for k in range(12)]

    def update_board(self, board, player):
        self.positionStates = []  #keeps track of AI board configuration
        self.boardStates = [] #keeps track of the mask
        self.playerCount['human'] = 0
        self.playerCount['computer'] = 0
        mask, position = '', ''
        for j in range(11, -1, -1):
            self.moves[str(j)] = 0
            position += '0'
            mask += '0'
            #start with the upper row
            for i in range(6):
                position += ['0', '1'][board[i, j] == player]
                mask += ['0', '1'][board[i, j] != 0]
                if board[i, j] != 0:
                    self.moves[str(j)] += 1
                    if board[i, j] == 1:
                        self.playerCount['human'] += 1
                    else :
                        self.playerCount['computer'] += 1
        self.position = int(position, 2)
        self.mask = int(mask, 2)

    def connected_four(self, position):
        #Horizontal check
        check = position & (position >> 7)
        if check & (check >> 14) : 
            return True

        #Diagonal \
        check = position & (position >> 6)
        if check & (check >> 12) : 
            return True

        #Diagonal /
        check = position & (position >> 8)
        if check & (check >> 16) : 
            return True

        #Vertical
        check = position & (position >> 1)
        if check & (check >> 2): 
            return True

        return False
    
    def make_move(self, col, mask, position, maxPlayer):
        newPosition = position ^ mask
        newMask = mask | (mask + (1 << (col*7))) #opponents turn, we switch to his board
        if maxPlayer :
            self.playerCount['computer'] += 1
        else :
            self.playerCount['human'] += 1
        self.moves[str(col)] += 1
        return newMask, newPosition
    
    def actions(self):
        return [int(column) for column in self.moves if self.moves[column] < 6] #Only if 5 pieces or less have been played in this column
    
    def utility(self, maxPlayer):#inverser
        pass

    def minimax(self, depth, alpha, beta, maxPlayer, mask=None, position=None):
        if mask == None:
            mask = deepcopy(self.mask)
            position = deepcopy(self.position)
        
        if depth == 0 or self.connected_four(position):
            score = self.utility(maxPlayer)
            if score < 0 :
                print(score)
            return [-1, score]
        
        if maxPlayer:
            maxScore = [-1, -inf]
            actions = self.actions()
            for action in actions:
                j = action
                newMask, newPosition = self.make_move(j, mask, position, maxPlayer)
                score = self.minimax(depth-1, alpha, beta, False, newMask, newPosition)
                self.playerCount['computer'] -= 1
                self.moves[str(action)] -= 1 #undo the move
                score[0] = j
                maxScore = maxScore if maxScore[1] >= score[1] else score
                if maxScore[1] >= beta:
                    return maxScore
                alpha = max(alpha, maxScore[1])
            return maxScore
        else:
            minScore = [-1, +inf]
            actions = self.actions()
            for action in actions:
                j = action
                newMask, newPosition = self.make_move(j, mask, position, maxPlayer)
                score = self.minimax(depth-1, alpha, beta, True, newMask, newPosition)
                self.playerCount['human'] -= 1
                self.moves[str(action)] -= 1 #undo the move
                score[0] = j
                minScore = minScore if minScore[1] <= score[1] else score
                if minScore[1] <= alpha: 
                    return minScore
                beta = min(beta, minScore[1])
            return minScore