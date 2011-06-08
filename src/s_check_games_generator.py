# -*- coding:utf-8 -*-
"""
Created on Jun 8, 2011

@author: inesmeya
"""
from random import Random
import random
import sys
import utils

GAME_SET_NAME = "gameset"
NUMBER_OF_GAME_PAIRS = 100

MIN_SIZE =  5
MAX_SIZE =  15

MAX_TIME = 20.0
MIN_TIME = 0.5

MIN_TURNS = 20
MAX_TURNS = 70



def generate_games(num_of_games,seed = None, setname =GAME_SET_NAME):
    
    if seed is None: 
        seed = random.randint(0,sys.maxint)
    
    rand = Random(seed)
    
    
    total_time = 0.0
    
    game_params_arr = [None]*num_of_games
    for i in range(0,num_of_games):
        
        board_size = rand.randint(MIN_SIZE,MAX_SIZE)
        turns = rand.randint(MIN_TURNS,MAX_TURNS)
        turn_time_limit = rand.uniform(0.5,MAX_TIME)
        
        game_params_arr[i] = {
            'size' : board_size,
            'turns_left' : turns,
        
            'turn_time_limit' : turn_time_limit,
            'setup_time_limit' : 10.0
        }
        
        time_for_game = turn_time_limit * float(turns) / 2.0
        total_time += time_for_game
    total_time_hours = total_time / 3600.0
    print "Total time hours for the '", setname, "' set (with seed=", seed, ") is ", total_time_hours
    return  game_params_arr

def save_games(games,name =GAME_SET_NAME):
    utils.pcl_psave(games, name)
    
def generate_and_save():
    games = generate_games(NUMBER_OF_GAME_PAIRS)
    save_games(games)


def load_games(name=GAME_SET_NAME):
    return  utils.pcl_load(name)

if __name__ == '__main__':
    generate_and_save()   
