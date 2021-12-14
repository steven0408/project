import numpy as np
import Gobang as go
import random

class player:
    def __init__(self):
        self.board = go.BuildBoard(8)
        self.valid_moves = [[i, j] for i in range(8) for j in range(8)]
        self.root = node()
        self.current_node = self.root
    
    def move(self, board, last_step, player):
        if not last_step:
            self.root.player = -player
            self.current_node = self.root
            next_step = random.choice(self.valid_moves)
            self.root_forward(next_step)
            return self.root.move
        else:
            self.root_forward(last_step)
            self.current_node = self.root
            next_step = random.choice(self.valid_moves)
            self.root_forward(next_step)
            return self.root.move
        
    def root_forward(self, next_step):
        if not self.root.children:
            self.root.expand(self.valid_moves)
        next_index = self.valid_moves.index(next_step)
        self.root = self.root.children[next_index]
        self.root.parrent = None
        self.board[next_step] = self.root.player
        self.valid_moves.remove(next_step)

    def forward(self, board, valid_moves, next_step, player):
        row, col = next_step
        assert board[row, col] == 0, "This position has another disc."
        board[row, col] = player
        assert next_step in valid_moves, "Next step is not in valid moves."
        valid_moves.remove(next_step)
        
    def selection(self, board, valid_moves):
        if self.current_node.isLeaf():
            return
        else:
            next_node = self.current_node.find_max_UCB_child()
            self.current_node = next_node
            self.forward(board, valid_moves, next_node.move, next_node.player)
            self.selection(board, valid_moves)
            
    def expansion(self, board, valid_moves):
        if not valid_moves:
            return
        else:
            self.current_node.expand(valid_moves)
            next_node = random.choice(self.current_node.children)
            self.forward(self, board, valid_moves, next_node.move, next_node.player)
            self.current_node = next_node
            
    def simulation(self, board, valid_moves)->int:
        current_player = -self.current_node.player
        while valid_moves:
            next_step = random.choice(valid_moves)
            self.forward(board, valid_moves, next_step, current_player)
            if IsContinuous(board, next_step):
                winner = current_player
                return winner
            else:
                current_player *= -1
        return 0

    
    
    
class node:
    def __init__(self, player=1, move=None, parent=None):
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
        assert self.children, "No child to find max UCB."
        idx = 0
        max_UCB = -float("inf")
        for i, child in enumerate(self.children):
            UCB = child.UCB(self.Ni)
            if UCB > max_UCB:
                idx = i
                max_UCB = UCB
        return self.children[idx]
    
    def find_max_score_child(self):
        assert self.children, "No child to find max score."
        idx = 0
        max_score = -float("inf")
        for i, child in enumerate(self.children):
            score = child.score()
            if score > max_score:
                idx = i
                max_score = score
        return self.children[idx]
    
    def isLeaf(self):
        if not self.children:
            return True
        else:
            return False
        
    def inTree(self):
        if self.Ni != 0:
            return True
        else:
            return False
        
    def expand(self, valid_moves):
        if not valid_moves:
            return
        for i in valid_moves:
            self.children.append(node(-self.player, i, self))
                
    def update(self, winner):
        self.Ni += 1
        if winner == self.player:
            self.Wi += 1
    
        
    