import math
from game import GameState, GameAction


#Global Constants
TIE = 'Tie'
WHITE = 'W'
BLACK = 'B'
EMPTY = ' '

class LinesOfActionState(GameState):
    '''
    A game state in Lines of Action.
    '''
    
    def __init__(self, size, turns_left, board = None, whites = None, blacks = None):
        '''
        Constructor.
        
        @param size: The board's width.
        @param turns_left: The number of turns left before an automatic tie.
        @param board: A matrix describing the board.
        @param whites: The number of white pieces.
        @param blacks: The number of black pieces.
        '''
        self.size = size
        self.turns_left = turns_left
        
        if board is None:
            self.board = []
            self.board += [(EMPTY,) + (WHITE,)*(size-2) + (EMPTY,)]
            for i in xrange(size - 2):
                self.board += [(BLACK,) + (EMPTY,)*(size-2) + (BLACK,)]
            self.board += [(EMPTY,) + (WHITE,)*(size-2) + (EMPTY,)]
            self.board = tuple(self.board)
            
            self.whites = 2*size - 4
            self.blacks = 2*size - 4
        else:
            self.board = board
            self.whites = whites
            self.blacks = blacks
    
    def getSuccessors(self):
        current_player = self.getCurrentPlayer()
        successors = {}
        for row, row_data in enumerate(self.board):
            for col, cell in enumerate(row_data):
                if cell == current_player:
                    for direction in DIRECTIONS:
                        action, state = self._getMoveAction(row, col, direction)
                        if action is not None:
                            successors[action] = state
                    for spin in [(row, col), (row - 1, col), (row, col - 1), (row - 1, col - 1)]:
                        action, state = self._getSpinAction(spin[0], spin[1])
                        if action is not None:
                            successors[action] = state
        return successors
    
    def getCurrentPlayer(self):
        '''
        White plays in even turns, black in odd. 
        '''
        if self.turns_left % 2 == 0:
            return WHITE
        else:
            return BLACK
    
    def getWinner(self):
        if self.turns_left == 0:
            return TIE
        
        white_wins = None
        black_wins = None
        for row, row_data in enumerate(self.board):
            for col, cell in enumerate(row_data):
                if cell == WHITE and white_wins is None:
                    component = self._getConnectiveComponent(row, col, WHITE)
                    white_wins = (len(component) == self.whites)
                if cell == BLACK and black_wins is None:
                    component = self._getConnectiveComponent(row, col, BLACK)
                    black_wins = (len(component) == self.blacks)
                
                if (white_wins is not None) and (black_wins is not None):
                    break
        
        if not white_wins and not black_wins:
            return None
        elif white_wins and not black_wins:
            return WHITE
        elif  black_wins and not white_wins:
            return BLACK
        else:
            return TIE
    
    def getTurnsLeft(self):
        return self.turns_left
    
    def _getMoveAction(self, row, col, direction):
        '''
        Checks the validity and the ramifications of performing a move action at the given location in the given direction.
        
        @param row: The row coordinate.
        @param col: The column coordinate.
        @param direction: The direction to move in.
        @return: The action and resulting state or None if illegal.
        '''
        distance = 1
        first_enemy = self.size
        
        (i_row, i_col) = direction.move((row, col))
        while (0 <= i_row < self.size) and (0 <= i_col < self.size):
            cell = self.board[i_row][i_col]
            if cell != EMPTY:
                distance += 1
                if cell != self.getCurrentPlayer() and first_enemy == self.size:
                    first_enemy = max(abs(row - i_row), abs(col - i_col))
            (i_row, i_col) = direction.move((i_row, i_col))
        
        opposite_direction = Direction('temp', (-direction.delta[0], -direction.delta[1]))
        (i_row, i_col) = opposite_direction.move((row, col))
        while (0 <= i_row < self.size) and (0 <= i_col < self.size):
            if self.board[i_row][i_col] != EMPTY:
                distance += 1
            (i_row, i_col) = opposite_direction.move((i_row, i_col))
        
        if distance > first_enemy:
            return None, None
        
        (new_row, new_col) = (direction.delta[0]*distance + row, direction.delta[1]*distance + col)
        if not ((0 <= new_row < self.size) and (0 <= new_col < self.size)):
            return None, None
        
        new_cell = self.board[new_row][new_col]
        if new_cell == self.getCurrentPlayer():
            return None, None
        
        if new_cell == WHITE:
            new_whites = self.whites - 1
        else:
            new_whites = self.whites
        
        if new_cell == BLACK:
            new_blacks = self.blacks - 1
        else:
            new_blacks = self.blacks
        
        new_board = list(self.board)
        
        new_board[row] = list(new_board[row])
        new_board[row][col] = EMPTY
        new_board[row] = tuple(new_board[row])
        
        new_board[new_row] = list(new_board[new_row])
        new_board[new_row][new_col] = self.getCurrentPlayer()
        new_board[new_row] = tuple(new_board[new_row])
        
        state = LinesOfActionState(self.size, self.turns_left - 1, tuple(new_board), new_whites, new_blacks)
        return (MoveAction(row, col, direction), state)
    
    def _getSpinAction(self, row, col):
        '''
        Checks the validity and the ramifications of performing a spin action at the given location.
        
        @param row: The row coordinate.
        @param col: The column coordinate.
        @return: The action and resulting state or None if illegal.
        '''
        if not ((0 <= row < self.size - 1) and (0 <= col < self.size - 1)):
            return None, None
        
        new_board = list(self.board)
        new_board[row] = list(new_board[row])
        new_board[row + 1] = list(new_board[row + 1])
        
        temp = new_board[row][col]
        new_board[row][col] = new_board[row + 1][col]
        new_board[row + 1][col] = new_board[row + 1][col + 1]
        new_board[row + 1][col + 1] = new_board[row][col + 1]
        new_board[row][col + 1] = temp
        
        new_board[row] = tuple(new_board[row])
        new_board[row + 1] = tuple(new_board[row + 1])
        
        state = LinesOfActionState(self.size, self.turns_left - 1, tuple(new_board), self.whites, self.blacks)
        return (SpinAction(row, col), state)
    
    def _getConnectiveComponent(self, initial_row, initial_col, player):
        '''
        Performs BFS to traverse the connective component, beginning at the given coordinate.
        
        @param initial_row: The initial row coordinate.
        @param initial_col: The initial column coordinate.
        @param player: The player who's connective component we would like to traverse.
        @return: The closed set - the connective component.
        '''
        open = set()
        open.add((initial_row, initial_col))
        closed = set()
        
        while len(open) > 0:
            (row, col) = open.pop()
            closed.add((row, col))
            for direction in DIRECTIONS:
                (neighbor_row, neighbor_col) = direction.move((row, col))
                if (0 <= neighbor_row < self.size) and (0 <= neighbor_col < self.size) \
                    and (self.board[neighbor_row][neighbor_col] == player) \
                    and ((neighbor_row, neighbor_col) not in closed):
                    open.add((neighbor_row, neighbor_col))
        
        return closed
    
    def __cmp__(self, other):
        return cmp((self.size, self.getCurrentPlayer(), self.turns_left, self.board), (other.size, other.getCurrentPlayer(), other.turns_left, other.board))
    
    def __hash__(self):
        return hash((self.size, self.getCurrentPlayer(), self.turns_left, self.board))
    
    def __str__(self):
        str_board = ''
        N = self.size
        minCellSize = int(math.floor(math.log10(N))+1)
        def justify(s):
            return str(s).rjust(minCellSize)
        str_board += justify('') + ' '
        for col_num in xrange(0, N):
            str_board += justify(col_num) + ' '
        str_board += '\n'
        row_num = 0
        for row in self.board:
            str_board += justify(row_num) + ' '
            for col in row:
                str_board += justify(col) + ' '
            str_board += '\n'
            row_num += 1
        return str_board


class MoveAction(GameAction):
    '''
    Moves a piece from the given location in the given direction.
    '''
    
    def __init__(self, row, col, direction):
        self.row = row
        self.col = col
        self.direction = direction
    
    def __cmp__(self, other):
        cType = cmp(self.__class__.__name__, other.__class__.__name__)
        if cType != 0:
            return cType
        else:
            return cmp((self.row, self.col, self.direction), (other.row, other.col, other.direction))
    
    def __hash__(self):
        return hash((self.row, self.col, self.direction))
    
    def __str__(self):
        return str((self.row, self.col)) + ' ' + str(self.direction)


class SpinAction(GameAction):
    '''
    Performs a 90 degree spin of a 2x2 square. The square is marked by the top-left corner.
    '''
    
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def __cmp__(self, other):
        cType = cmp(self.__class__.__name__, other.__class__.__name__)
        if cType != 0:
            return cType
        else:
            return cmp((self.row, self.col), (other.row, other.col))
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def __str__(self):
        return str((self.row, self.col)) + ' spin'


class Direction():
    '''
    A direction of movement.
    '''
    
    def __init__(self, name, delta):
        '''
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction (row_delta, col_delta).
        '''
        self.name = name
        self.delta = delta
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        return cmp(self.name, other.name)
    
    def __hash__(self):
        '''
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        '''
        return hash(self.name)
    
    def __str__(self):
        '''
        @return: The string representation of this object when *str* is called.
        '''
        return str(self.name)
    
    def __repr__(self):
        return self.__str__()
    
    def move(self, location):
        '''
        @return: Moving from the given location in this direction will result in the returned location.
        '''
        return (location[0] + self.delta[0], location[1] + self.delta[1])

#Global Directions
DIRECTIONS = (Direction("N", (-1, 0)), 
              Direction("E", (0, 1)), 
              Direction("S", (1, 0)), 
              Direction("W", (0, -1)), 
              Direction("NE", (-1, 1)), 
              Direction("SE", (1, 1)), 
              Direction("SW", (1, -1)), 
              Direction("NW", (-1, -1)))

