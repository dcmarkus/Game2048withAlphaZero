# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 21:45:37 2019

@author: Prava
Nural network and loss function
"""

import random
import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


"""
Alphaloss is implimented
"""

    
class AlphaLoss(torch.nn.Module):
    def __init__(self):
        super(AlphaLoss, self).__init__()

    def forward(self, y_value, value, y_policy, policy):
        value_error = (value - y_value) ** 2
        policy_error = torch.sum((-policy* 
                                (1e-8 + y_policy.float()).float().log()),0)
        total_error = (value_error.view(-1).float() + policy_error).mean()
        return total_error

"""
This neural network takes 16 inputs and gives 5 outputs. It has 4 hidden leyer
"""
#class Network(nn.Module):
#    def __init__(self):
#        super().__init__()
#        
#        # Inputs to hidden layer linear transformation
#        self.hidden = nn.Linear(16, 600)
#        self.hidden1 = nn.Linear(600,600)
#        self.hidden2 = nn.Linear(600,600)
#        self.hidden3 = nn.Linear(600,600)
#        self.hidden4 = nn.Linear(600,600)
#        self.hidden5 = nn.Linear(600,600)
#        self.hidden6 = nn.Linear(600,600)
#        self.hidden7 = nn.Linear(600,600)
#        self.hidden8 = nn.Linear(600,600)
#        self.hidden9 = nn.Linear(600,500)
#        self.output = nn.Linear(500, 5)
#        
#        # Define sigmoid activation and softmax output 
#        self.sigmoid = nn.Sigmoid()
#        self.softmax = nn.Softmax(dim=0)
#        
#        
#    def forward(self, x):
#        # Pass the input tensor through each of our operations
#        x = self.hidden(x)
#        x = self.sigmoid(x)
#        x = self.hidden1(x)
#        x = self.sigmoid(x)
#        x = self.hidden2(x)
#        x = self.sigmoid(x)
#        x = self.hidden3(x)
#        x = self.sigmoid(x)
#        x = self.hidden4(x)
#        x = self.sigmoid(x)
#        x = self.hidden5(x)
#        x = self.sigmoid(x)
#        x = self.hidden6(x)
#        x = self.sigmoid(x)
#        x = self.hidden7(x)
#        x = self.sigmoid(x)
#        x = self.hidden7(x)
#        x = self.sigmoid(x)
#        x = self.hidden9(x)
#        x = self.sigmoid(x)
#        x = self.output(x)
#        x = self.sigmoid(x)
#        probs = self.softmax(x[0:4])#softmax makes the total probability 1
#        
#        
#        return (x,probs)

class Network(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Inputs to hidden layer linear transformation
        self.hidden = nn.Linear(16, 300)
        self.hidden1 = nn.Linear(300,300)
        self.hidden2 = nn.Linear(300,300)
        self.hidden3 = nn.Linear(300,500)
        self.output = nn.Linear(500, 5)
        
        # Define sigmoid activation and softmax output 
        self.sigmoid = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=0)
        
    def forward(self, x):
        # Pass the input tensor through each of our operations
        x = self.hidden(x)
        x = self.sigmoid(x)
        x = self.hidden1(x)
        x = self.sigmoid(x)
        x = self.hidden2(x)
        x = self.sigmoid(x)
        x = self.hidden3(x)
        x = self.sigmoid(x)
        x = self.output(x)
        x = self.sigmoid(x)
        
        probs = self.softmax(x[0:4])#softmax makes the total probability 1
        
        
        return (x,probs)
net = Network()


criterion = AlphaLoss()# AlphaZero Loss function as defined above
#criterion = nn.MSELoss()#MSE Loss function
#%%

#State =torch.tensor([2.,  4., 16.,  2.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
#         0.,  0.])
#probpred = torch.tensor([0.2495, 0.2513, 0.2436, 0.2556])
#    
#output = net(State)
#print(output[1])
##%%
##
#optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.005)
#
#epochs = 3000
#running_loss = 0
#for e in range(epochs):
#    
#    
#    # Training pass
#    optimizer.zero_grad()
#    probpred = torch.tensor([0.2495, 0.2513, 0.2436, 0.2556])
#    
#    output = net(State)
#    loss = criterion(output[0][-1],1.0,output[1],probpred)
#
#
#    print(loss)
#    optimizer.zero_grad()   # zero the gradient buffers
#    loss.backward()
#    optimizer.step()
#    
#    running_loss += loss.item()
##   
##%%
#print(net(State))