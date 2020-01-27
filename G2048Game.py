# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:38:53 2019

@author: David
"""
from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from G2048Board import Board
import numpy as np

class G2048Game(Game):


    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return 4

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = Board(self.n)
        #print(board)
        b.pieces = np.copy(board)
        #print(b.pieces)
        b.execute_move(action, player)
        #print("NS",b.pieces)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        for j in range(self.n):
            for i in range(self.n-1):
                if b.pieces[i][j]==0 or abs(b.pieces[i][j])==abs(b.pieces[i+1][j]):
                    valids[0]=1
        for j in range(self.n):
            for i in range(self.n-1):
                if b.pieces[1+i][j]==0 or abs(b.pieces[i+1][j])==abs(b.pieces[i][j]):
                    valids[3]=1
        for i in range(self.n):
            for j in range(self.n-1):
                if b.pieces[i][1+j]==0 or abs(b.pieces[i][1+j])==abs(b.pieces[i][j]):
                    valids[1]=1
        for i in range(self.n):
            for j in range(self.n-1):
                if b.pieces[i][j]==0 or abs(b.pieces[i][j+1])==abs(b.pieces[i][j]):
                    valids[2]=1
        return valids

    def getGameEnded(self, board, player):
        t=self.getValidMoves(board,player)
        if sum(t)!=0:
            return 0
        b = Board(self.n)
        b.pieces = np.copy(board)
        mat=b.pieces
        cur_max=2
        cur_winner=0
        game_end_i=True
        for i in range(len(mat)): 
            for j in range(len(mat[0])):
                if abs(mat[i][j])>cur_max:
                    cur_max=abs(mat[i][j])
                    cur_winner=np.sign(mat[i][j])
                if abs(mat[i][j])==cur_max and cur_winner!=np.sign(mat[i][j]):
                    game_end_i=False
        if game_end_i:
            return cur_winner
        point_list=[0]*2 
        for i in range(len(mat)): 
            for j in range(len(mat[0])):
                if np.sign(mat[i][j])!=-1:
                    point_list[np.sign(mat[i][j])]=point_list[np.sign(mat[i][j])]+np.abs(mat[i][j])
        
        point_list_sort=sorted(point_list)
        
        if point_list[-1]==point_list[-2]:
            return -1
        return(np.argmax(point_list))

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        #print("Hallo ",len(pi))
#        assert(len(pi) == 4)  # 1 for pass
#        pi_board = np.reshape(pi[:-1], (self.n, self.n))
#        l = []
#
#        for i in range(1, 5):
#            for j in [True, False]:
#                newB = np.rot90(board, i)
#                newPi = np.rot90(pi_board, i)
#                if j:
#                    newB = np.fliplr(newB)
#                    newPi = np.fliplr(newPi)
#                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
#        return l
        n=[(board,pi)]
        return n

    def stringRepresentation(self, board):
        return board.tostring()

    #def getScore(self, board, player):
    #    b = Board(self.n)
    #    b.pieces = np.copy(board)
    #    return b.countDiff(player)

    @staticmethod
    def display(board):
        n = board.shape[0]
        print("   ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")
        print("-----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                print(piece[0]*piece[1], end=" ")
            print("|")

        print("-----------------------")
