
class QuadTable():

    def __init__(self, board, size, player):
        '''
        Constructor.
        
        @param size: The board's width.
        @param board: A matrix describing the board.
        @param player: The player (Black/White) which the quad table describes.
        '''
        self.size = size
        self.board = board
        self.player = player
        self.quads = {}
        
        for x in range(-1, size):
            for y in range(-1, size):
                self.quads[(x,y)] = findQuadType(x, y, board, size, player)

    def getQuadType(self, x, y):
        return self.quads[(x,y)]
    
    def eulerNumber(self):
        q1 = 0
        q3 = 0
        qd = 0
        
        for x in range(-1, self.size):
            for y in range(-1, self.size):
                if self.quads[(x,y)] == 'Q1':
                    q1 += 1
                elif self.quads[(x,y)] == 'Q3':
                    q3 += 1
                elif self.quads[(x,y)] == 'Qd':
                    print x, ',', y
                    qd += 1
                    
                    
        print 'W:', 'Q1 = ', q1, 'Q3 = ', q3, 'Qd = ', qd
        return float(q1-q3-2*qd)/4

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
        
        