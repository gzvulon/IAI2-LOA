# A bloody large number.
from s_heuristics import simple_heuristic, winner_heuristics
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
            # TODO: here we have an action, hence we can pass it to heuristic fn
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
        successors = state.getSuccessors()
        ordered_successors = successors #f_reorder_max(state,successors)
        for successor in ordered_successors.values():
            value_fn = self._getValueFn(successor)
            value = max(value, value_fn(successor, alpha, beta, depth + 1))
            if value >= beta: # cut
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
            if value <= alpha: # cut
                return value
            beta = min(beta, value)
        
        return value

# winner_check options
QUAD_WINNER = True
SIMPLE_WINNER = False
#----------------------

#


class SmartAlphaBetaSearch:
    '''
    This search algorithm implements the limited-resource minimax tree search 
    algorithm with alpha-beta pruning for zero-sum games. This version cuts off 
    search by depth alone and uses an evaluation function (utility).
    '''
    
    def __init__(self, player, max_depth, utility, winner_check=SIMPLE_WINNER):
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
        self.quad_table = None
        
        self.f_checkWinner = { 
            SIMPLE_WINNER: self._checkWinnerSimple,
            QUAD_WINNER:   self._checkWinnerEuler,
        }[winner_check]

    
    def search(self, current_state, max_depth):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param current_state: The current game state to start the search from.
        '''
        best_value = -INFINITY
        successors = current_state.getSuccessors()
        
        for action, state in successors.items():
            state_info = {} #todo initiate state info
            value = self._minValue(state, best_value, INFINITY, 1,max_depth, state_info)
            
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    
    def _need_return(self,state, depth, max_depth,info_set):
        ''' checks if node terminal or reached depth limit =X
        @return: True, value if X  if node terminal or reached depth limit,
                       value - node value
                 False,0 - otherwise
        '''
        # check if node is terminate
        w = self.f_checkWinner(state)
        # if it is : return its value (-1 for enemy, +1 for us)
        if w != 0:
            return True,w
        
        # if reached depth limit: evaluate node using heuristics
        if depth >= max_depth:
            return True, self.utility(state, info_set) # new_info_set        
        
        return False,0
    
    def _maxValue(self, state, alpha, beta, depth,max_depth, info_set):
        
        need_return, v = self._need_return(state, depth, max_depth,info_set)
        if need_return: return v
        
        # -- on regular node : use improved alpha beta --
        
        value = -INFINITY
        successors = state.getSuccessors()
        # -- reordering --
        #ordered_successors = self.f_oreder(successors,depth,max_depth)
        
        for action, successor_state in successors.items():
            # update iterative info for son node
            new_info_set = self._update_info_set(info_set, state, action, successor_state)
            # calculate minimum for son
            min_value = self._minValue(successor_state, alpha, beta, depth + 1,max_depth, new_info_set )
            value = max(value,min_value)
            if value >= beta: # cut
                return value 
            alpha = max(alpha, value)
        # save partial results
        return value
    
    def _minValue(self, state, alpha, beta, depth,max_depth,info_set):
        
        need_return, v = self._need_return(state, depth, max_depth,info_set)
        if need_return: return v
        
        value = INFINITY
        successors = state.getSuccessors()
        # -- reordering --
        #ordered_successors = self.f_oreder(successors,depth,max_depth)
        
        for action, successor_state in successors.items():
            # update iterative info for son node
            new_info_set = self._update_info_set(info_set, state, action, successor_state)
            max_value = self._maxValue(successor_state, alpha, beta, depth + 1,max_depth,new_info_set)
            
            value = min(value,max_value)
            if value <= alpha: # cut
                return value
            beta = min(beta, value)
        
        return value
    
    # ========================= Geneneral ==============================
    #todo: test is
    def _update_info_set(self,info_dict, state, action, successor_state):
        new_info_dict = {}
        for k,v in info_dict:
            new_info_dict[k] = v.update(state, action, successor_state)
        return new_info_dict
    
    
    
    # =========================  OPTIONS ===============================
    # ------------------------  check winner options --------------------
    def _checkWinnerSimple(self,state):
        ''' returns 0 if no winner, otherwise us +1 they: -1
        '''
        r =  winner_heuristics(state,self.player)
        return r
    
    def _checkWinnerEuler(self,state):
        ''' returns 0 if no winner, otherwise us +1 they: -1
        '''
        quad_table = ""
        euler_number = quad_table.eulerNumber(self.player)
        
        if euler_number > 1.0:
            return 0
        else:
            return self._checkWinnerSimple(state)
    # ------------------------   end check winner options  --------------------   

    def _updateNothig(self,state, action, new_state):
        pass
