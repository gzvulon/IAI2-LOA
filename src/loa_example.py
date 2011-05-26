from game_runner import GameRunner
from loa_game import WHITE, BLACK, LinesOfActionState, SpinAction, MoveAction, DIRECTIONS, Direction
from game_agent import GameAgent
from alpha_beta import AlphaBetaSearch
from code import interact

class DummyAgent(GameAgent):
    def move(self, game_state):
        for action in game_state.getSuccessors().keys():
            return action
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        return

class AlphaBetaAgent(GameAgent):
    def move(self, game_state):
        return self.alphaBeta.search(game_state)
    
    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        u = lambda state: self.utility(state)
        self.alphaBeta = AlphaBetaSearch(self.player, 3, u)

    def utility(self, state):
        winner = state.getWinner()
        if winner is None:
            return 0
        elif winner == self.player:
            return 1
        else:
            return -1
        
class InteractiveAgent(GameAgent):
    def move(self, game_state):
        print game_state
        inp = raw_input(self.player + ' turn. Enter <row col action> (action is N/NE/E/SE/S/SW/W/NW/SPIN): ')
        row, col, action = inp.split()
        row = int(row)
        col = int(col)
        action = action.upper()
        res = []
        if(action == 'SPIN'):
            res = SpinAction(row, col)
        else:
            direction_idx = DIRECTIONS.index(Direction(action, (0, 0)))
            res = MoveAction(row, col, DIRECTIONS[direction_idx])
        return res           

    def setup(self, player, game_state, turn_time_limit, setup_time_limit):
        self.player = player
        
    
agents = {}
agents[WHITE] = AlphaBetaAgent()
agents[BLACK] = DummyAgent()

state = LinesOfActionState(6, 50)


winner = GameRunner(state, agents, 2, 1).run()
print 'Winner:', winner
