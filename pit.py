import Arena
from MCTS import MCTS
from MCTSwithoutNN import MCTSnn
from G2048Game import G2048Game as Game
from NNet import NNetWrapper as nn
import torch
import AlphaZero_with_pytorch as alpha


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


def redefine(mat):
    matnew=[[(0,0)]*len(mat)]*len(mat)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                matnew[i][j][0]=0
                matnew[i][j][1]=-1
            else:
                matnew[i][j][0]=np.abs(mat[i][j])
                matnew[i][j][1]=np.sign(mat[i][j])

g = Game(5)

# all players
rp = RandomPlayer(g).play


# nnet players
n1 = nn(g)
checkpoint=torch.load("best.pth.tar")
n1.nnet.load_state_dict(checkpoint['state_dict'])
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

n2 = nn(g)
checkpoint=torch.load("checkpoint_2.pth.tar")
n2.nnet.load_state_dict(checkpoint['state_dict'])
args2 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts2 = MCTSnn(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

#n2p=lambda x: alpha.alphaZeroSearch()


arena = Arena.Arena(n1p, n2p, g, display=None)

print(arena.playGames(10, verbose=False))
