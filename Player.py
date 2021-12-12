import numpy as np
import Gobang as go
import random

class player:
    def __init__(self):
        self.tree = tree()
        pass
    
    def move(self, board, laststep):
        return random.choice(go.GetValid(board))
    
class node:
    def __init__(self, player=None, move=None, parent=None):
        self.player = player
        self.move = move
        self.Ni = 0
        self.Wi = 0
        self.parrent = None
        self.children = []
        
    def UCB(self, N, c=np.sqrt(2*np.log(2)/np.log(np.e))):
        if self.Ni == 0:
            return(float("inf"))
        elif N == 0:
            return self.Wi/self.Ni
        else:
            return self.Wi/self.Ni + c*np.sqrt(np.log(N)/self.Ni)
        
    def score(self):
        if self.Ni == 0:
            return 0
        else:
            return self.Wi/self.Ni
        
    def find_max_UCB_child(self):
        idx = 0
        max_UCB = -float("inf")
        for i, child in enumerate(self.children):
            UCB = child.UCB(self.Ni)
            if UCB > max_UCB:
                idx = i
                max_UCB = UCB
        return self.children[idx]
    
class tree:
    def __init__(self):
        self.board = go.BuildBoard(8)
        self.root = node()
        
    