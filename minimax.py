# -*- coding: utf-8 -*-


import random
import numpy as np
import math
import copy

import logic1
import constants as c


def alphaBetaSearch(mat,player):
    v = maxValue(mat,player,-math.inf,math.inf,optimalDepth(mat,player))#deoth taken from depth function
    #print(v[0])
    action = v[1] # the action in {up,down,left,right} with value v[0]
    # search the correct key
    if action == 0:       # Action: UP
        key = c.KEY_UP
    elif action == 1:     # Action: LEFT
        key = c.KEY_LEFT
    elif action == 2:     # Action: RIGHT
        key = c.KEY_RIGHT
    elif action == 3:     # Action: DOWN
        key = c.KEY_DOWN
    # return the correct key
    return key

def maxValue(mat,player,alpha,beta,depth):
    if terminalTest(mat) or depth == 0:
        return (utility(mat,player),-1)      #-1 irrelevant for depth>0
    depth = depth - 1
    v = -math.inf
    aBest = -1
    for a in range (0, 4):  #four possible moves (up,down,left,right)
        res = result(mat,player,a)
        if res is None: #Check for the possibility of the move
            continue
        vSum = 0
        average = 0
        # Go through all possibilities of random place
        for i in range(0, c.GRID_LEN):
            for j in range(0, c.GRID_LEN):
                if (res[i][j][0] != 0): # Check possibility
                    continue
                res[i][j] = (2,(player+1)%2) # Set the random tile
                vTemp = minValue(res,player,alpha,beta,depth)[0]
                # v = max(v, vTemp)
                vSum = vSum + vTemp
                average = average + 1
                res[i][j] = (0,-1) # Undo the random tile for iteration
        vAverage = vSum/average
        if vAverage > v:
            v = vAverage
            aBest = a
        if v >= beta:
            return (v,aBest)
        alpha = max(alpha,v)
    return (v,aBest)

def minValue(mat,player,alpha,beta,depth):
    if terminalTest(mat) or depth == 0:
        return (utility(mat,player),-1)      #-1 irrelevant for depth>0
    depth = depth - 1
    v = math.inf
    aBest = -1
    for a in range (0, 4):  #four possible moves (up,down,left,right)
        res = result(mat,player,a)
        if res is None: #Check for the possibility of the move
            continue
        vSum = 0
        average = 0
        # Go through all possibilities of random place
        for i in range(0, c.GRID_LEN):
            for j in range(0, c.GRID_LEN):
                if (res[i][j][0] != 0): # Check possibility
                    continue
                res[i][j] = (2,(player+1)%2) # Set the random tile
                vTemp = maxValue(res,player,alpha,beta,depth)[0]
                # v = min(v, vTemp)
                vSum = vSum + vTemp
                average = average + 1
                res[i][j] = (0,-1) # Undo the random tile for iteration
        vAverage = vSum/average
        if vAverage < v:
            v = vAverage
            aBest = a
        if v <= alpha:
            return (v,aBest)
        beta = min(beta,v)
    return (v,aBest)

# A terminal test, which is true when the game is over and false otherwise
def terminalTest(mat):
    return (logic1.game_state(mat) != 'not over')

# A utility function defines the numeric value for a game that ends in state mat
def utility(mat,player):    # 0=Red, 1=Blue
    acc = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j][0]==0:
                continue
            temp = mat[i][j][0]*math.pow(10,math.log2(mat[i][j][0])-1)
            if mat[i][j][1] == player:  # add this tile to acc
                acc = acc + temp
            else:                       # sub this tile from acc
                acc = acc - temp
    return acc

# The transition model, which defines the result of a move
def result(mat,player,action):
    if action == 0:       # Action: UP
        res = logic1.up(mat,player)
    elif action == 1:     # Action: LEFT
        res = logic1.left(mat,player)
    elif action == 2:     # Action: RIGHT
        res = logic1.right(mat,player)
    else:                 # Action: DOWN
        res = logic1.down(mat,player)
    if res[1]:
        return res[0]
    else:
        return None

# BETA
# Calculate the optimal depth for good performance
def optimalDepth(mat,player):
    MAGIC_BOUND = 100000
    statesNumber = 1
    for a in range (0, 4):  #four possible moves (up,down,left,right)
        res = result(mat,player,a)
        if res is None: #Check for the possibility of the move
            continue
        # Go through all possibilities of random place
        for i in range(0, c.GRID_LEN):
            for j in range(0, c.GRID_LEN):
                if (res[i][j][0] == 0): # Check possibility
                    statesNumber = statesNumber + 1
    # statesNumber^depth < MAGIC_BOUND
    depth = math.floor(math.log2(MAGIC_BOUND)/math.log2(statesNumber))
    if depth <=2:
        depth = 1
    else:
        depth = 3
    #print(depth)
    return depth
