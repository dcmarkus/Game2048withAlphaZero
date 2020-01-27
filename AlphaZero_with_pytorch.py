import random
import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import Nnet1

import logic1
import constants as c

"""
Function loads the saved neural network. It is called later in alphaZeroTrain in test part.
Function calls neural network model from Nnnet. It also calls saved data from ckeckpoint.pth.
"""
def load_checkpoint(filepath):
    checkpoint = torch.load(filepath)
    model = Nnet1.net
    model.load_state_dict(checkpoint['model_state_dict'])
    for parameter in model.parameters():
        parameter.requires_grad = True

    model.eval()
    return model



"""
Function alphaZerosearch has two conditions. Train the model and test the model.
"""



def alphaZeroSearch(mat,player,numberOfPlaythroughs,hyperC,Test,Player):
    # DO MONTE-CARLO-TREE-SEARCH

    possibilities = getPossibilities(mat,player)

    """
    Save the State.
    """
    State =torch.zeros(16)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            State[i]=(mat[i][j][0])
    State

    # Play the game a number of times and count the action numbers in the counters
    actionVisitCounter = torch.tensor([0, 0, 0, 0.],dtype =torch.float) # Number, how often action is was visited in MCTS
    actionEndCounter = torch.tensor([0, 0, 0, 0.],dtype =torch.float) # Number, how often action was picked first 
    actionWinCounter = torch.tensor([0, 0, 0, 0.],dtype =torch.float) # Number, how often action was picked first for win
    Umax = -math.inf
    """
    If the test is False then its for traning.
    """
    if Test == False:#for  training
       
        for i in range(0,numberOfPlaythroughs):
            actionVisitCounter, actionEndCounter, actionWinCounter = randomPlay(mat,player,actionVisitCounter,actionEndCounter,actionWinCounter,State)#Taking laste value fro NN
        
    
 
        
        # Search the best action
        
        U = []
        q = actionWinCounter/actionEndCounter
        
        N = sum(actionEndCounter)
        bestAction = -1
        for i in range(0,len(possibilities)):
#            action = possibilities[i]
#            Utemp = q[action]+hyperC*math.sqrt(math.log(N)/actionEndCounter[action])
#            U.append(Utemp)
            action = possibilities[i]
            res = result(mat,player,action)
            q = utility(res,player)
            p = 1/len(possibilities)
            nominator = math.sqrt(sum(actionWinCounter))
            denominator = 1 + actionWinCounter[action]
            Utemp = q+hyperC*p*nominator/denominator
            if (Utemp>Umax):
                Umax = Utemp
                bestAction = action
#
        #print(U)
    
        # Search the correct key
        if bestAction == 0:       # Action: UP
            key = c.KEY_UP
        elif bestAction == 1:     # Action: LEFT
            key = c.KEY_LEFT
        elif bestAction == 2:     # Action: RIGHT
            key = c.KEY_RIGHT
        elif bestAction == 3:     # Action: DOWN
            key = c.KEY_DOWN
        # Return the correct key
        #print(actionWinCounter)
        return (key,State.tolist(),np.array(actionWinCounter))#actionWinC/actionendcounter 


    
    if Test == True:#In test phase

    
#       To text NN Vs NN
        if  Player == 1 :# for compitition between trained and un trained neural network
            SavedNetwork = load_checkpoint('Utility_function30.pth')
            outputValue = SavedNetwork(State)[0][-1]# Z value of the state
            #print(outputValue)
            while outputValue >0:
                actionWinCounter = SavedNetwork(State)[1]
               
                
                for i in range(0,len(possibilities)):
                    action = possibilities[i]
                    Utemp = actionWinCounter[action]
                  
                    
                    if (Utemp>Umax):
                        Umax = Utemp
                        bestAction = action
                        
                
                return bestAction
            
            
        if Player == 2:
            SavedNetwork = load_checkpoint('Best1.pth')
            
            outputValue = SavedNetwork(State)[0][-1]# Z value of the state
            #print(outputValue)
            while outputValue >0:
                actionWinCounter = SavedNetwork(State)[1]
               
                
                for i in range(0,len(possibilities)):
                    action = possibilities[i]
                    
                    res = result(mat,player,action)
                    q = utility(res,player)
                    p = 1/len(possibilities)
                    nominator = math.sqrt(sum(actionWinCounter))
                    denominator = 1 + actionWinCounter[action]
                    Utemp = q+hyperC*p*nominator/denominator
                    Utemp = actionWinCounter[action]
                  
                    
                    if (Utemp>Umax):
                        Umax = Utemp
                        bestAction = action
                        
                # Search the correct key
                if bestAction == 0:       # Action: UP
                    key = c.KEY_UP
                elif bestAction == 1:     # Action: LEFT
                    key = c.KEY_LEFT
                elif bestAction == 2:     # Action: RIGHT
                    key = c.KEY_RIGHT
                elif bestAction == 3:     # Action: DOWN
                    key = c.KEY_DOWN
                # Return the correct key
                
                return key#actionWinC/actionendcounter 

# A terminal test, which is true when the game is over and false otherwise
def terminalTest(mat):
    return (logic1.game_state(mat) != 'not over')

# A function to play random and update the counters
def randomPlay(mat,player,actionVisitCounter,actionEndCounter,actionWinCounter,State):
    tempPlayer = player
    firstActionChoice = -1
    MCnet = Nnet1.net#load_checkpoint('Winner0_40.pth')
    while (False == terminalTest(mat)):
        possibilities = getPossibilities(mat,tempPlayer)
        probs = [0,0,0,0]
        # Get here probability distribution p from NN
        
        #
        
        pNN= MCnet(State)[1]
        #print(sum(pNN))
        #pNN = normalize(pNN)
        
        #pNN = [0,0,0,0]
        numberOfPossibilites = len(possibilities)
        for i in range (0, numberOfPossibilites):
            pNN[possibilities[i]] = 1/numberOfPossibilites
        # The sum of the entries of p should be 1
        for i in range (0,len(possibilities)):
            actionIndex = possibilities[i]
            probs[actionIndex] = pNN[actionIndex]
            probs = normalize(probs)
        rn = random.random()
        cnt=0.0
        for i in range(len(probs)):
            cnt+=probs[i]
            if rn <= cnt:
                randomAction=i
                break
        #randomAction = np.random.choice([0,1,2,3],1,p=probs)[0]
        #print(randomAction)
        if (firstActionChoice == -1):
            firstActionChoice = randomAction
        actionVisitCounter[randomAction] = actionVisitCounter[randomAction] + 1
        mat = result(mat,tempPlayer,randomAction)
        tempPlayer = (tempPlayer+1)%2
        mat = logic1.add_two(mat,tempPlayer)
    actionEndCounter[firstActionChoice] = actionEndCounter[firstActionChoice] + 1
    if ("draw" == logic1.game_state(mat)):
        return actionVisitCounter, actionEndCounter, actionWinCounter
    elif (player == logic1.game_state(mat)-1):
        actionWinCounter[firstActionChoice] = actionWinCounter[firstActionChoice] + 1
        return actionVisitCounter, actionEndCounter, actionWinCounter
    else: #Oppenent has won
        return actionVisitCounter, actionEndCounter, actionWinCounter

# Get possible moves of a given state with player
def getPossibilities(mat,player):
   

    possibilities = []
    for a in range (0, 4):  #four possible moves (up,down,left,right)
        res = result(mat,player,a)
        if res is None: #Check for the possibility of the move
            continue
        else:
            possibilities.append(a)
  
    
    
    
    return possibilities
# Normalize probs such that the sum of all entries of probs is 1
def normalize(probs):
    normalizer = 1/sum(probs)
    for i in range (0,len(probs)):
        probs[i] = probs[i]*normalizer
    return probs


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
#%%Test
#State =torch.tensor([2.,  4., 16.,  2.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.])
#probpred = torch.tensor([0.2495, 0.2513, 0.2436, 0.2556])
#SavedNetwork = load_checkpoint('Train_Data\Without.pth')    
#output = SavedNetwork(State)
#print(output)