# A bloody large number.
INFINITY = 1.0e400

class AlphaBetaSearch:
    '''
    This search algorithm implements the limited-resource minimax tree search 
    algorithm with alpha-beta pruning for zero-sum games. This version cuts off 
    search by depth alone and uses an evaluation function (utility).
    '''
    
    def __init__(self, player, max_depth, utility):
        '''
        Constructor.
        
        @param player: Your player. This search algorithm will choose the best
                       actions for this player.
        @param max_depth: The depth of the search tree.
        @param utility: An evaluation function for states.
        '''
        self.player = player
        self.max_depth = max_depth
        self.utility = utility
    
    def search(self, current_state):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param current_state: The current game state to start the search from.
        '''
        best_value = -INFINITY
        
        for action, state in current_state.getSuccessors().items():
            value_fn = self._getValueFn(state)
            value = value_fn(state, best_value, INFINITY, 1)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    def _getValueFn(self, state):
        if state.getCurrentPlayer() == self.player:
            return self._maxValue
        else:
            return self._minValue
    
    def _cutoffTest(self, state, depth):
        return depth >= self.max_depth or (state.getWinner() is not None)
    
    def _maxValue(self, state, alpha, beta, depth):
        if self._cutoffTest(state, depth):
            return self.utility(state)
        
        value = -INFINITY
        for successor in state.getSuccessors().values():
            value_fn = self._getValueFn(successor)
            value = max(value, value_fn(successor, alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        
        return value
    
    def _minValue(self, state, alpha, beta, depth):
        if self._cutoffTest(state, depth):
            return self.utility(state)
        
        value = INFINITY
        for successor in state.getSuccessors().values():
            value_fn = self._getValueFn(successor)
            value = min(value, value_fn(successor, alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        
        return value
