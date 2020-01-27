# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:39:22 2019

@author: David
"""
import random
import numpy as np

class Board():


    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [None]*self.n
        for i in range(self.n):
            for j in range(self.n):
                self.pieces[i][j]=0

        # Set up the initial 4 pieces.
        # self.pieces[int(self.n/2)-1][int(self.n/2)] = 1
        # self.pieces[int(self.n/2)][int(self.n/2)-1] = 1
        # self.pieces[int(self.n/2)-1][int(self.n/2)-1] = -1;
        # self.pieces[int(self.n/2)][int(self.n/2)] = -1;
        self.add_two(1)
        self.add_two(1)
        self.add_two(-1)
        self.add_two(-1)
        
    def __getitem__(self, index): 
        return self.pieces[index]
        
        
    def add_two(self,player):
        check=[]
        for i in range(self.n):
            for j in range(self.n):
                if self.pieces[i][j] == 0:
                    check.append((i,j))
        #print(check)
        r=random.randint(0,len(check)-1)
        t=check[r]
        self.pieces[t[0]][t[1]] = player*2

        
    def reverse(self,mat):
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[i][len(mat)-j-1])
        return np.array(new)


    def transpose(self,mat):
        new = []
        for i in range(len(mat)):
            new.append([])
            for j in range(len(mat)):
                new[i].append(mat[j][i])
        return np.array(new)
    
    
    
    def cover_up(self,mat):
        new = []
        for i in range(len(mat)):
            new.append([0] * len(mat))
        done = False
        for i in range(len(mat)):
            count = 0
            for j in range(len(mat)):
                if mat[i][j] != 0:
                    new[i][count] = mat[i][j]
                    if j != count:
                        done = True
                    count += 1
        return (np.array(new), done)
    
    
    def merge(self,mat,x):
        done = False
        for i in range(len(mat)):#Changed So that merge can happed for dimensions other then 4X4 
            for j in range(len(mat)-1):
                #print(type(mat[i][j]))
                #print(mat[i][j])
                if np.abs(mat[i][j]) == np.abs(mat[i][j+1]) and mat[i][j] != 0:# and (mat[i][j]==mat[i][j+1] or np.sign(mat[i][j+1])==x):
                    mat[i][j] = mat[i][j+1]*2
                    mat[i][j+1] = 0
                    done = True
        return (mat, done)
    
    
    def up(self,game,x):
        #print("up")
        # return matrix after shifting up
        game = self.transpose(game)
        game, done = self.cover_up(game)
        temp = self.merge(game,x)
        game = temp[0]
        done = done or temp[1]
        game = self.cover_up(game)[0]
        game = self.transpose(game)
        return (np.array(game), done)
    
    
    def down(self,game,x):
        #print("down")
        game = self.reverse(self.transpose(game))
        game, done = self.cover_up(game)
        temp = self.merge(game,x)
        game = temp[0]
        done = done or temp[1]
        game = self.cover_up(game)[0]
        game = self.transpose(self.reverse(game))
        return (np.array(game), done)
    
    
    def left(self,game,x):
        #print("left")
        # return matrix after shifting left
        game, done = self.cover_up(game)
        temp = self.merge(game,x)
        game = temp[0]
        done = done or temp[1]
        game = self.cover_up(game)[0]
        return (np.array(game), done)
    
    
    def right(self,game,x):
        #print("right")
        # return matrix after shifting right
        game = self.reverse(game)
        game, done = self.cover_up(game)
        temp = self.merge(game,x)
        game = temp[0]
        done = done or temp[1]
        game = self.cover_up(game)[0]
        game = self.reverse(game)
        return (np.array(game), done)



    def execute_move(self, action, player):
        if action == 0:       # Action: UP
            res = self.up(self.pieces,player)
        elif action == 1:     # Action: LEFT
            res = self.left(self.pieces,player)
        elif action == 2:     # Action: RIGHT
            res = self.right(self.pieces,player)
        else:                 # Action: DOWN
            res = self.down(self.pieces,player)
        
        self.pieces=res[0]
        self.add_two(player)
        return True



