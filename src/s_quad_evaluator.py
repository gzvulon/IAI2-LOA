'''
Created on Jun 7, 2011

@author: hizki
'''
from s_enums import QUAD_TABLE_TAG

class QuadEvaluator():
    
    def evaluate(self, state, player, info_set):
        
        quad_table = info_set[QUAD_TABLE_TAG]
        euler = quad_table.eulerNumber(player)
        
        if euler > 1:
            return 1 / euler
        else:
            return 1