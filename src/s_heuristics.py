from loa_game import EMPTY

def winner_heuristics(state,player):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1

def make_simple_heuristic(player):
    '''
    @param player: player 

    @return: heuristics functions for provided player
    @type return: fn: state -> double in range [-1.0;1.0]
    '''
    def the_heuristic(state):
        return winner_heuristics(player,state)

    return the_heuristic    

def simple_heuristic(player):
    '''
    @param player: player 

    @return: heuristics functions for provided player
    @type return: fn: state -> double in range [-1.0;1.0]
    '''
    def the_heuristic(state):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == player:
            return 1
        else:
            return -1
    
    return the_heuristic

def not_simple_heuristic(player):
    
    def the_heuristic(state, quadTable):
        groups_bonus = 0    
        for x in range(-1, state.size):
            for y in range(-1, state.size):
                quadType = quadTable.quads[(x,y)]
                if quadType == 'Q3' or quadType == 'Q4':
                    groups_bonus += 1

        edges_penalty = 0
        for x in range(-1, state.size):
            if state.board[0][x] != EMPTY:
                edges_penalty += 1
            if state.board[state.size-1][x] != EMPTY:
                edges_penalty += 1
        for y in range(-1, state.size):
            if state.board[y][0] != EMPTY:
                edges_penalty += 1
            if state.board[y][state.size-1] != EMPTY:
                edges_penalty += 1                
                        
        
    return the_heuristic