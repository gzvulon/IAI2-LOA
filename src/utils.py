# -*- coding:utf-8 -*-
"""
Created on May 4, 2011

@author: inesmeya
"""
import pickle

def pload(path):
    with open(path,"r") as file:
        o = pickle.load(file)
    return o

def psave(obj,path):
    with open(path, "w+") as file:
        pickle.dump(obj, file)