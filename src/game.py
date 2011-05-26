class GameState:
    
    def getSuccessors(self):
        '''
        Generates all the actions that can be performed from this state, and
        the States those actions will create.
        
        @return: A dictionary containing each action as a key, and its state.
        '''
        raise NotImplementedError()
    
    def getCurrentPlayer(self):
        '''
        @return: The player that should play next.
        '''
        raise NotImplementedError()
    
    def getWinner(self):
        '''
        @return: The winner of the game, according to this state. 
        Returns None if this state is not terminal.
        '''
        raise NotImplementedError()
    
    def getTurnsLeft(self):
        '''
        @return: The number of turns left before the game ends.
        None is returned if the game is unlimited.
        '''
        raise NotImplementedError()
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        raise NotImplementedError()
    
    def __hash__(self):
        '''
        The hash method must be implemented for states to be inserted into sets 
        and dictionaries.
        @return: The hash value of the state.
        '''
        raise NotImplementedError()
    
    def __str__(self):
        raise NotImplementedError()
    
    def __repr__(self):
        return self.__str__()
    
class GameAction:
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        raise NotImplementedError()
    
    def __hash__(self):
        '''
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        '''
        raise NotImplementedError()
    
    def __str__(self):
        '''
        @return: The string representation of this object when *str* is called.
        '''
        raise NotImplementedError()
    
    def __repr__(self):
        '''
        Same as __str__, unless overridden.
        
        @return: The string representation of this object when *printed*.
        '''
        return self.__str__()
