from s_definitions import EMPTY, WHITE, BLACK
from bundlebuilder import copy
from loa_game import MoveAction


class QuadTable():

    def __init__(self, board, size):
        '''
        Constructor.
        
        @param size: The board's width.
        @param board: A matrix describing the board.
        '''
        self.size = size
        self.board = board
        self.white_quads = {}
        self.black_quads = {}
        
        for x in range(-1, size):
            for y in range(-1, size):
                self.setQuadType(x, y, findQuadType(x, y, board, size, WHITE), WHITE)
                self.setQuadType(x, y, findQuadType(x, y, board, size, BLACK), BLACK)

    def getQuadType(self, x, y, player):
        if x >= -1 and x < self.size and y >=-1 and y < self.size:
            if player == WHITE:
                return self.white_quads[(x,y)]
            elif player == BLACK:
                return self.black_quads[(x,y)]
        return None
    
    def setQuadType(self, x, y, type, player):
        if x >= -1 and x < self.size and y >=-1 and y < self.size: 
            if player == WHITE:
                self.white_quads[(x,y)] = type
            elif player == BLACK:
                self.black_quads[(x,y)] = type
    
    def eulerNumber(self, player):
        q1 = 0
        q3 = 0
        qd = 0
        
        for x in range(-1, self.size):
            for y in range(-1, self.size):
                quadType = self.getQuadType(x, y, player)
                if quadType == 'Q1':
                    q1 += 1
                elif quadType == 'Q3':
                    q3 += 1
                elif quadType == 'Qd':
                    qd += 1
                    
        return float(q1-q3-2*qd)/4


    def update(self, state, action, newstate):
        newQuadTable = copy(self)
        if isinstance(action, MoveAction):
            newQuadTable.movePiece(action, state.getCurrentPlayer)
            

    def movePiece(self, action, player):
        from_x = action.col
        from_y = action.row
        
        to_y, to_x = findDest(action, board, size)
        
        self.board[from_y][from_x] = EMPTY
        if self.board[to_y][to_x] == other_player(player):
            capture = True
            
        self.board[to_y][to_x] = player
        
        self.updateSurroundingCells(from_x, from_y, player)
        self.updateSurroundingCells(to_x, to_y, player)
        if capture:
            self.updateSurroundingCells(to_x, to_y, other_player(player))




    def updateSurroundingCells(self, x, y, player):
        self.setQuadType(x, y, findQuadType(x, y, self.board, self.size, player), player)
        self.setQuadType(x-1, y, findQuadType(x-1, y, self.board, self.size, player), player)
        self.setQuadType(x, y-1, findQuadType(x, y-1, self.board, self.size, player), player)
        self.setQuadType(x-1, y-1, findQuadType(x-1, y-1, self.board, self.size, player), player)

def findDest(action):
    dist = calcMoveDist(action)
    to_x = action.col + dist * action.direction.delta[1]
    to_y = action.row + dist * action.direction.delta[0]
    return to_y, to_x
        
def calcMoveDist(action, board, size):
#        print '----'
    dist = 0
    x = action.col
    y = action.row
    while x >= 0 and y >= 0 and x < size and y < size:
#            print '(',x,',',y,') = ', board[y][x]
        if board[y][x] != EMPTY:
            dist += 1
        x += action.direction.delta[1]
        y += action.direction.delta[0]
    
#        print '+++'

    x = action.col
    y = action.row
    while x >= 0 and y >= 0 and x < size and y < size:
#            print '(',x,',',y,') = ', board[y][x]
        if board[y][x] != EMPTY:
            dist += 1
        x += -action.direction.delta[1]
        y += -action.direction.delta[0]
    
    return dist - 1
             
def findQuadType(x, y, board, size, player):
    filled = 0
    
    if y >= 0 and x >= 0 and board[y][x] == player:
        filled += 1
    if y+1 < size and x >= 0 and board[y+1][x] == player:
        filled += 1      
    if y >= 0 and x+1 < size and board[y][x+1] == player:
        filled += 1
    if y+1 < size and x+1 < size and board[y+1][x+1] == player:
        filled += 1
    
    if filled == 0:
        return 'Q0'
    if filled == 1:
        return 'Q1'
    elif filled == 3:
        return 'Q3'
    elif filled == 4:
        return 'Q4'
    elif filled == 2:
        if x >= 0 and x+1 < size and y >= 0 and y+1 < size:
            if board[y][x] == board[y+1][x+1] or board[y+1][x] == board[y][x+1]:
                return 'Qd'
            else:
                return 'Q2'
        else:
            return 'Q2'


def other_player(player):
    if player == WHITE:
        return BLACK
    elif player == BLACK:
        return WHITE
    else:
        return EMPTY
