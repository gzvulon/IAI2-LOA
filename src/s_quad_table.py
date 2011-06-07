from loa_game import MoveAction, WHITE, BLACK, EMPTY
from s_common_ops import findQuadType, other_player, findDest
from copy import copy


class QuadTable():

    def __init__(self, board, size, white_quads = None, black_quads = None, initialize = True):
        '''
        Constructor.
        
        @param size: The board's width.
        @param board: A matrix describing the board.
        '''
        self.size = size
        self.board = board

        if white_quads != None:
            self.white_quads = white_quads
        else:
            self.white_quads = {}
        
        if black_quads != None:
            self.black_quads = black_quads
        else:
            self.black_quads = {}             
        
        if initialize:
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


    def update(self, state, newstate, action):
        # Create a new quad table to be updated and returned.
        cwq = copy(self.white_quads)
        cbq = copy(self.black_quads)
        newQuadTable = QuadTable(newstate.board, self.size, cwq, cbq, 
                                                            initialize = False)
        
        # Check which action was made.
        if isinstance(action, MoveAction):
            newQuadTable.movePiece(action, state)
        else: # is instance of SpinAction
            newQuadTable.spin(action, state)

        return newQuadTable


    def updateWithoutAction(self, state, newstate):
        # Create a new quad table to be updated and returned.
        cwq = copy(self.white_quads)
        cbq = copy(self.black_quads)
        newQuadTable = QuadTable(newstate.board, self.size, cwq, cbq, 
                                                            initialize = False)
        
        # find which cells where changed, and update the corresponding quads.
        for x in range(0, state.size):
            for y in range(0, state.size):
                if state.board[y][x] != newstate.board[y][x]:
                    for player in [WHITE, BLACK]:
                        newQuadTable.updateSurroundingCells(x, y, player)

        return newQuadTable

    def spin(self, action, state):
        for player in [WHITE, BLACK]:
            for x in range(action.col-1, action.col+2):
                for y in range(action.row-1, action.row+2):
                    self.setQuadType(x, y, findQuadType(x, y, self.board, 
                                                    self.size, player), player)

    def movePiece(self, action, state):
        from_x = action.col
        from_y = action.row
        player = state.board[action.row][action.col]
        
        to_y, to_x = findDest(action, state.board, state.size)
        
        capture = False
        if state.board[to_y][to_x] == other_player(player):
            capture = True
            
        self.updateSurroundingCells(from_x, from_y, player)
        self.updateSurroundingCells(to_x, to_y, player)
        if capture:
            self.updateSurroundingCells(to_x, to_y, other_player(player))


    def updateSurroundingCells(self, x, y, player):
        self.setQuadType(x, y, findQuadType(x, y, self.board, self.size, player), player)
        self.setQuadType(x-1, y, findQuadType(x-1, y, self.board, self.size, player), player)
        self.setQuadType(x, y-1, findQuadType(x, y-1, self.board, self.size, player), player)
        self.setQuadType(x-1, y-1, findQuadType(x-1, y-1, self.board, self.size, player), player)


    def __eq__(self, other):
        if self.size != other.size:
            return False

        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if self.black_quads[(x,y)] != other.black_quads[(x,y)]:
                    return False
                if self.white_quads[(x,y)] != other.white_quads[(x,y)]:
                    return False
                
        return True

 
    def __ne__(self, other):
        return not self.__eq__(other)

def create_QuadTable(state, action=None, newstate =None):
    res = QuadTable(state.board, state.size, initialize = True)
    return res

def update(target_state, old_q_table, old_state, action):
    old_q_table.update(old_state,target_state,action)
    

class QuadTableNoUpdate(QuadTable):
    def __init__(self, *args, **kwds):
        QuadTable.__init__(self, *args, **kwds)
    
    def update(self, state, newstate, action):
        return QuadTableNoUpdate(state.board, state.size, initialize=True)
    
    def updateWithoutAction(self, state, newstate):
        return QuadTableNoUpdate(state.board, state.size, initialize=True)  
        

class QuadTableDoesNothing():
    
    def update(self, *args):
        return self
    
    def updateWithoutAction(self, *args):
        return self  
        
    
        