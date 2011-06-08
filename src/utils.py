# -*- coding:utf-8 -*-
"""
Created on May 4, 2011

@author: inesmeya
"""
import pickle
import os

def pload(path):
    with open(path,"r") as file:
        o = pickle.load(file)
    return o
 
def psave(obj,path):
    with open(path, "w+") as file:
        pickle.dump(obj, file)
        

def pcl_load(path):
    path += ".pcl"
    with open(path,"r") as file:
        o = pickle.load(file)
    return o
 
def pcl_psave(obj,path):
    path += ".pcl"
    with open(path, "w+") as file:
        pickle.dump(obj, file)