
class QuadTable():

    def __init__(self, board, size, player):
        '''
        Constructor.
        
        @param size: The board's width.
        @param board: A matrix describing the board.
        @param player: The player (Black/White) which the quad table describes.
        '''
        self.quads = {}
        
        for x in range(-1, size):
            for y in range(-1, size):
                self.quads[(x,y)] = findQuadType(x, y, board, size, player)

    def getQuadType(self, x, y):
        return self.quads[(x,y)]

def findQuadType(x, y, board, size, player):
    filled = 0
    
    if x >= 0 and y >= 0 and board[x][y] == player:
        filled += 1
    if x+1 < size and y >= 0 and board[x+1][y] == player:
        filled += 1      
    if x >= 0 and y+1 < size and board[x][y+1] == player:
        filled += 1
    if x+1 < size and y+1 < size and board[x+1][y+1] == player:
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
            if board[x][y] == board[x+1][y+1] or board[x+1][y] == board[x][y+1]:
                return 'Qd'
            else:
                return 'Q2'
        else:
            return 'Q2'
        
        