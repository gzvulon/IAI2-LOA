from loa_game import WHITE, BLACK, EMPTY
import time

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
    
    
    
# --------------  Time -------------------------------
class TimeOutException(Exception):
    pass

def checkTime(end_time, safe_delta=0):
    '''raises exception on timeout type: TimeOutException'''
    if(end_time - safe_delta < time.clock()):
        raise TimeOutException()
    
    