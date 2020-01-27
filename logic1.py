# -*- coding: utf-8 -*-
import random
import numpy as np
import constants as c

def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([(0,-1)] * n)
    return matrix


def add_two(mat,x):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while(mat[a][b][0] != 0):
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = (2,x)
    return mat



def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j][0] == 1048576:#^2**20
                winner=mat[i][j][1]+1
                return winner
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j][0] == mat[i+1][j][0] or mat[i][j+1][0] == mat[i][j][0]:
                return 'not over'
    for i in range(len(mat)):  # check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j][0] == 0:
                return 'not over'
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k][0] == mat[len(mat)-1][k+1][0]:
            return 'not over'
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1][0] == mat[j+1][len(mat)-1][0]:
            return 'not over'
    cur_max=2
    cur_winner=-1
    game_end_i=True
    for i in range(len(mat)): 
        for j in range(len(mat[0])):
            if mat[i][j][0]>cur_max:
                cur_max=mat[i][j][0]
                cur_winner=mat[i][j][1]
            if mat[i][j][0]==cur_max and cur_winner!=mat[i][j][1]:
                game_end_i=False
    if game_end_i:
        return cur_winner+1
    point_list=[0]*2 #replace with number of players if implemented
    for i in range(len(mat)): 
        for j in range(len(mat[0])):
            if mat[i][j][1]!=-1:
                point_list[mat[i][j][1]]=point_list[mat[i][j][1]]+mat[i][j][0]
    
    point_list_sort=sorted(point_list)
    
    if point_list[-1]==point_list[-2]:
        return "draw"
    #print(point_list_sort[1])
    return(np.argmax(point_list)+1)


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new



def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new



def cover_up(mat):
    new = new_game(len(mat))
    done = False
    for i in range(len(mat)):
        count = 0
        for j in range(len(mat)):
            if mat[i][j][0] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return (new, done)


def merge(mat,x):
    done = False
    for i in range(c.GRID_LEN):#Changed So that merge can happed for dimensions other then 4X4 
        for j in range(c.GRID_LEN-1):
            if mat[i][j][0] == mat[i][j+1][0] and mat[i][j][0] != 0 and (mat[i][j][1]==mat[i][j+1][1] or mat[i][j+1][1]==x):
                mat[i][j] = (mat[i][j][0]*2, mat[i][j+1][1])
                mat[i][j+1] = (0,-1)
                done = True
    return (mat, done)


def up(game,x):
    #print("up")
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    temp = merge(game,x)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(game)
    return (game, done)


def down(game,x):
    #print("down")
    game = reverse(transpose(game))
    game, done = cover_up(game)
    temp = merge(game,x)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return (game, done)


def left(game,x):
    #print("left")
    # return matrix after shifting left
    game, done = cover_up(game)
    temp = merge(game,x)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    return (game, done)


def right(game,x):
    #print("right")
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    temp = merge(game,x)
    game = temp[0]
    done = done or temp[1]
    game = cover_up(game)[0]
    game = reverse(game)
    return (game, done)
