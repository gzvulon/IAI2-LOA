NO_LIMIT = -1

class GameAgent ():
    '''
    This is an interface for a Game Playing Agent.
    '''
    
    def move(self, game_state):
        '''
        This is the method called by the runner of this agent.
        It includes the code that decides the next move.
        
        @param game_state: The current game state.
        @return: The GameAction that the agent will execute in its next move.
        '''
        raise NotImplementedError()
    
    def setup(self, player, game_state, turn_time_limit = NO_LIMIT, setup_time_limit = NO_LIMIT):
        '''
        This is method is called once at the beginning of the game, 
        and enables the agent to prepare for things to come.
        
        @param player: Your player.
        @param game_state: The initial game state.
        @param turn_time_limit: The time that will be allocated for each turn.
        @param setup_time_limit: The time limit for setting up this agent.
        '''
        raise NotImplementedError()
