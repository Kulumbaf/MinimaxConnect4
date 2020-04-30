#12*6 connect 4
from copy import deepcopy
from math import inf
from collections import defaultdict

class Minimax:
    def __init__(self, board, player):
        self.maxDepth = 6 #The AI will see 6 plays further
        self.configure_dict()
        self.update_board(board, player)

    def configure_dict(self):
        '''
        We will use default dict to keep track of the moves and avoid the AI to play on a full column
        '''
        self.moves = defaultdict(int)
        self.playerCount = defaultdict(int)
        [self.moves[str(k)] for k in range(12)]

    def update_board(self, board, player):
        '''
        This function init the bitboard and track the number of tokens per column
        '''
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
                    elif board[i, j] == 2 :
                        self.playerCount['computer'] += 1
        self.position = int(position, 2)
        self.mask = int(mask, 2)

    def count_set_bits(self, check):
        '''
        This fonction count the number of bits set to one in a binary representation of an integer
        '''
        count = 0
        while (check): 
            count += check & 1
            check >>= 1
        return count 

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
    
    def connected_three(self, computer, human, maxPlayer):
        '''
        Return the number of dangerous 3 in a row (not blocked yet)
        '''
        numberOfThrees = [0, 0]

        #Horizontal check
        check = computer & (computer >> 7)
        check = check & (check >> 7)
        check = check >> 7
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 7)
        check = check & (check << 7)
        check = check << 7
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 7)
        check = check & (check >> 7)
        check = check >> 7
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 7)
        check = check & (check << 7)
        check = check << 7
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)

        #Diagonal check \
        check = computer & (computer >> 6)
        check = check & (check >> 6)
        check = check >> 6
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 6)
        check = check & (check << 6)
        check = check << 6
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 6)
        check = check & (check >> 6)
        check = check >> 6
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 6)
        check = check & (check << 6)
        check = check << 6
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)

        #Diagonal check /
        check = computer & (computer >> 8)
        check = check & (check >> 8)
        check = check >> 8
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 8)
        check = check & (check << 8)
        check = check << 8
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 8)
        check = check & (check >> 8)
        check = check >> 8
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 8)
        check = check & (check << 8)
        check = check << 8
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)

        #Vertical check 
        check = computer & (computer >> 1)
        check = check & (check >> 1)
        check = check >> 1
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 1)
        check = check & (check << 1)
        check = check << 1
        comparator = check & human
        check = check - comparator
        numberOfThrees[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 1)
        check = check & (check >> 1)
        check = check >> 1
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 1)
        check = check & (check << 1)
        check = check << 1
        comparator = check & computer
        check = check - comparator
        numberOfThrees[1] += self.count_set_bits(check)

        return numberOfThrees
        
    def connected_two(self, computer, human, maxPlayer):
        '''
        Return the number of dangerous two in a row (a 3 in a row count as 2)
        '''
        numberOfTwos = [0, 0]

        #Horizontal check
        check = computer & (computer >> 7)
        check = check >> 7
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 7)
        check = check << 7
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 7)
        check = check >> 7
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 7)
        check = check << 7
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)

        #Diagonal check \
        check = computer & (computer >> 6)
        check = check >> 6
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 6)
        check = check << 6
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 6)
        check = check >> 6
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 6)
        check = check << 6
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)

        #Diagonal check /
        check = computer & (computer >> 8)
        check = check >> 8
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 8)
        check = check << 8
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 8)
        check = check >> 8
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 8)
        check = check << 8
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)

        #Vertical check 
        check = computer & (computer >> 1)
        check = check >> 1
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #Horizontal check backward
        check = computer & (computer << 1)
        check = check << 1
        comparator = check & human
        check = check - comparator
        numberOfTwos[0] += self.count_set_bits(check)
        #human
        check = human & (human >> 1)
        check = check >> 1
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)
        #human backward
        check = human & (human << 1)
        check = check << 1
        comparator = check & computer
        check = check - comparator
        numberOfTwos[1] += self.count_set_bits(check)

        return numberOfTwos

    def make_move(self, col, mask, position, maxPlayer):
        '''
        This function add a token on the top of the bitboard and update the position board to be the opponent's one
        '''
        newPosition = position ^ mask #opponents turn, we switch to his board
        newMask = mask | (mask + (1 << (col*7)))
        if maxPlayer :
            self.playerCount['computer'] += 1
        else :
            self.playerCount['human'] += 1
        self.moves[str(col)] += 1
        return newMask, newPosition
    
    def actions(self):
        '''
        Here we verify in the dictionnaries if a column is full of token or not and thus return the possible moves
        '''
        return [int(column) for column in self.moves if self.moves[column] < 6] #Only if 5 pieces or less have been played in this column
    
    def utility(self, depth, mask, position, maxPlayer):
        '''
        Heuristic function, better detailled on my website
        '''
        computer = position if maxPlayer else (position ^ mask)
        human = position if not maxPlayer else (position ^ mask)
        
        if self.connected_four(computer):
            return (10000 - (self.maxDepth - depth))
        if self.connected_four(human):
            return -(10000 - (self.maxDepth - depth))
        else:
            numberOfThrees = self.connected_three(computer, human, maxPlayer)
            numberOfTwos = self.connected_two(computer, human, maxPlayer)
            return (3*numberOfThrees[0] + numberOfTwos[0] - (3*numberOfThrees[1] + numberOfTwos[1]))

    def minimax(self, depth, alpha, beta, maxPlayer, mask=None, position=None):
        '''
        this minimax recursive function, test 6 moves further and call the utility function to score the boards.
        It then, take the best rated board and goes up on the tree to return the column to play in order to reach this specific board
        We assume that the opponent plays perfectly
        '''
        if mask == None:
            mask = deepcopy(self.mask)
            position = deepcopy(self.position)
        
        if depth == 0 or self.connected_four(position):
            score = self.utility(depth, mask, position, maxPlayer)
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