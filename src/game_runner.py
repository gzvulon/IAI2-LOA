from time import clock

class GameRunner():
    '''
    Runs a game.
    '''
    
    def __init__(self, initial_state, agents, turn_time_limit, setup_time_limit):
        '''
        Constructor.
        
        @param initial_state: The initial game state.
        @param agents: A dictionary that maps players to their agents.
        @param turn_time_limit: The time limit of each turn.
        @param setup_time_limit: The time limit for setting up the agent.
        '''
        self.initial_state = initial_state
        self.agents = agents
        self.turn_time_limit = turn_time_limit
        self.setup_time_limit = setup_time_limit
    
    def run(self):
        '''
        Runs the game. Prints actions and states.
        
        @return: The game's winner.
        '''
        for player, agent in self.agents.items():
            start = clock()
            agent.setup(player, self.initial_state, self.turn_time_limit, self.setup_time_limit)
            setup_time = clock() - start
            if setup_time > self.setup_time_limit:
                raise Exception(str(player) + ' failed to set up in time.')
        
        state = self.initial_state
        while state.getWinner() is None:
            agent = self.agents[state.getCurrentPlayer()]
            start = clock()
            action = agent.move(state)
            turn_time = clock() - start
            if turn_time > self.turn_time_limit:
                raise Exception(str(state.getCurrentPlayer()) + ' failed to return a move in time.')
            
            successors = state.getSuccessors()
            if action not in successors.keys():
                raise Exception(str(state.getCurrentPlayer()) + ' made an illegal move.')
            
            state = successors[action]
            
            print action
            print state
        
        return state.getWinner()
 