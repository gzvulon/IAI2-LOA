from s_heuristics import winner_heuristics
from random import Random
import time
from s_end_timer import checkTime, TimeOutException
from s_turn_cache import TurnCache, NoneTurnCache
from loa_game import LinesOfActionState
from s_end_timer import EndTimer
from s_statistics import GTimeStatistics
from s_common_ops import random_tag
from s_quad_table import QuadTable
import s_quad_table

# A bloody large number.
INFINITY = 1.0e400

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
    
    def __init__(self, player, utility, turn_cache, winner_check=SIMPLE_WINNER):
        '''
        Constructor.
        
        @param player: Your player. This search algorithm will choose the best
                       actions for this player.
        @param max_depth: The depth of the search tree.
        @param utility: An evaluation function for states.
        '''
        self.player = player
        self.turn_cache = turn_cache
        #self.max_depth = max_depth
        self.utility = utility
        self.quad_table = None
        #self.info_
        
        self.f_checkWinner = { 
            SIMPLE_WINNER: self._checkWinnerSimple,
            QUAD_WINNER:   self._checkWinnerEuler,
        }[winner_check]

    
    def search(self, current_state, max_depth, end_time, quad_table):
        '''
        Search game to determine best action; use alpha-beta pruning.
        
        @param current_state: The current game state to start the search from.
        @return: best_action, best_state
        '''
        # on each search this is renewed!
        self.end_time = end_time
        #
        best_value = -INFINITY
        
       
        
        EndTimer.check(name="a")
        #successors = current_state.getSuccessors()
        successors = self.turn_cache.get(current_state, LinesOfActionState.getSuccessors)
        
        
        EndTimer.check(name="a1")
        
        for action, state in successors.items():
            
            #quad_table_next = quad_table.update(current_state, action, state)
            EndTimer.check(name="b")
            
            state_info = {} #todo initiate state info
            value = self._minValue(state, best_value, INFINITY, 1,max_depth, state_info)
            
            if value > best_value:
                best_value = value
                best_action = action
                best_state  = state
        
        return best_action, best_state
    
    
    def _need_return(self,state, depth, max_depth,info_set):
        ''' checks if node terminal or reached depth limit =X
        @return: True, value if X  if node terminal or reached depth limit,
                       value - node value
                 False,0 - continue searching
        '''
        checkTime(self.end_time)
        # check if node is terminate
        w = self.f_checkWinner(state)
        # if it is : return its value (-1 for enemy, +1 for us)
        if w != 0:
            return True,w
        
        EndTimer.check(name="c")
        # if reached depth limit: evaluate node using heuristics
        if depth >= max_depth:
            u_res = self.turn_cache.get(state, self.utility, self.end_time)
            return True, u_res# self.utility(state) # new_info_set        
        
        return False,0
    
    def _maxValue(self, state, alpha, beta, depth,max_depth, info_set):
        
        need_return, v = self._need_return(state, depth, max_depth,info_set)
        if need_return: return v
        
        # -- on regular node : use improved alpha beta --
        
        value = -INFINITY
        EndTimer.check(name="d1")
        #successors = state.getSuccessors()
        successors = self.turn_cache.get(state, LinesOfActionState.getSuccessors)
        # -- reordering --
        #ordered_successors = self.f_oreder(successors,depth,max_depth)
        
        EndTimer.check(name="d2")
        str_key = "_maxValue.successors.items()  d:{0} tag{1}".format(depth,random_tag())
        GTimeStatistics.start_measure(str_key)
        successors_items = successors.items()
        GTimeStatistics.stop_measure(str_key)
        
        for action, successor_state in successors_items:
            
            EndTimer.check(name="d3")
           
            # update iterative info for son node
            new_info_set = self._update_info_set(info_set, state, action, successor_state)
            # calculate minimum for son
            EndTimer.check(name="e")
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
        
        EndTimer.check(name="f")
        #successors = state.getSuccessors()
        successors = self.turn_cache.get(state, LinesOfActionState.getSuccessors)
        
        # -- reordering --
        #ordered_successors = self.f_oreder(successors,depth,max_depth)
        str_key = "_minValue.successors.items() d:{0} tag{1}".format(depth,random_tag())
        GTimeStatistics.start_measure(str_key)
        successors_items = successors.items()
        GTimeStatistics.stop_measure(str_key)
        
        for action, successor_state in successors_items:
            EndTimer.check(name="g")
            # update iterative info for son node
            new_info_set = self._update_info_set(info_set, state, action, successor_state)
            EndTimer.check(name="h")
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
        return new_info_dict
#        for k,v in info_dict:
#            new_info_dict[k] = v.update(state, action, successor_state)
#        return new_info_dict
    
    # =========================  OPTIONS ===============================
    # ------------------------  check winner options --------------------
    def _checkWinnerSimple(self,state):
        ''' returns 0 if no winner, otherwise us +1 they: -1
        '''
        
        #winner = state.getWinner()
        winner = self.turn_cache.get(state, LinesOfActionState.getWinner)
        if winner is None:
            r = 0
        elif winner == self.player:
            r = 1
        else:
            r = -1
        
        return r
    
    def _checkWinnerEuler(self,state):
        ''' returns 0 if no winner, otherwise us +1 they: -1
        '''
        #TODO: add cache
        quad_table = ""
        euler_number = quad_table.eulerNumber(self.player)
        
        if euler_number > 1.0:
            return 0
        else:
            return self._checkWinnerSimple(state)
    # ------------------------   end check winner options  --------------------   

    def _updateNothig(self,state, action, new_state):
        pass


class AnyTimeSmartAlphaBeta():
    '''The Main Shit'''
    
    def get_name(self):
        return "AnyTimeSmartAlphaBeta"
    
    def __init__(self, player, init_max_depth, 
                 utility, winner_check=SIMPLE_WINNER, 
                 depth_delta=1, caching =False):
        self.player = player
        self.init_max_depth = init_max_depth
        self.utility = utility
        self.winner_check = winner_check
        self.rand = Random(0)
        self.depth_delta = depth_delta
        
        if caching: self.turn_cache = TurnCache()
        else:       self.turn_cache = NoneTurnCache()
        
            
    def search(self, current_state, max_depth, time_limit):
        #init timer
        safe_delta = 0.08
        start_time = time.clock()
        end_time   = start_time + time_limit - safe_delta
        EndTimer.set(end_time)
        #
        quad_table =  None #self.turn_cache.get(current_state,s_quad_table.create_QuadTable)
        
        #turn_info
        
        succesors = self.turn_cache.get(current_state, LinesOfActionState.getSuccessors)
        
        # choose default move randomly: 
        index = self.rand.randint(0, len(succesors)-1)
        res_action, res_state = succesors.items()[index] 
        
        # start iterative search
        curr_max_depth = self.init_max_depth
        # print "time left", end_time - time.clock(), "d=", curr_max_depth
        
        try:
            while time.clock() < end_time:
                print  "time left", end_time - time.clock(), "d=", curr_max_depth
                alg = SmartAlphaBetaSearch(self.player, self.utility, self.turn_cache, self.winner_check)
                res_action,res_state = alg.search(current_state, curr_max_depth, end_time, quad_table)
                curr_max_depth += self.depth_delta #TODO: TODO
        except TimeOutException: #TODO for release handle all exceptios
            pass
        
        EndTimer.stop()
        return res_action,res_state     
        
        