import numpy as np
import Gobang as go
import random
import multiprocessing as mp

constant_c = np.sqrt(2*np.log(2)/np.log(np.e))

class player:
    def __init__(self):
        self.turn = 0
    
    def move(self, board, last_step, player):
        if not last_step:
            return random.choice([[3, 3], [3, 4], [4, 3], [4, 4]])
        else:
            root = Node(-player, last_step, None, board.copy(), None)
            # next_step = random.choice(self.valid_moves)
            next_node, suggest = self.MCTS(root, len(np.argwhere(board != 0))*250) # 新增 suggest，型態是dictionary
            return next_node.move, suggest
        
    def selection(self, node):
        current = node
        while not current.isLeaf():
            current = current.find_max_UCB_child()
        assert current.isLeaf(), "Select a none leaf node!"
        return current
            
    def MCTS(self, root, max_total):
        total = 0
        while total < max_total:
            selected_node = self.selection(root)
            Ni = 0
            record = {1:0, -1:0, 0:0}
            if go.IsContinuous(selected_node.board, selected_node.move):
                Ni += 1
                record[selected_node.player] += 1
                selected_node.backpropagation(Ni, record)
            else:
                selected_node.expand()
                for j in selected_node.children:
                    winner = j.simulation()
                    Ni += 1
                    record[winner] += 1
                selected_node.backpropagation(Ni, record)
            total += Ni
        suggest = {0:[], 1:[]} # 0: cordinates, 1: win rates
        for i in root.children:
            suggest[0].append(i.move)
            suggest[1].append(i.Wi/i.Ni)
        # print(suggest)
        return root.find_max_score_child(), suggest
    
class Node:
    def __init__(self, player, move, parent, board, valid_moves):
        assert move, "Move should not be None."
        if not parent:
            assert not valid_moves, "Root should not have valid moves."
        self.player = player
        self.move = move
        self.Ni = 0
        self.Wi = 0
        self.parent = parent
        self.children = []
        self.board = board
        self.valid_moves = valid_moves if parent else self.update_valid_moves(move, board, [], root=True)
        
    def UCB(self, N, c=constant_c):
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
    
    def update(self, winner):
        self.Ni += 1
        if winner == self.player:
            self.Wi += 1
    
    def isLeaf(self):
        if not self.children:
            return True
        else:
            return False
        
    def update_valid_moves(self, move, board, valid_moves, root=False): # update valid_moves inplace
        x, y = move
        assert board[x, y], "Board must be update first."
        if root:
            assert not valid_moves, "Root valid moves should be empty."
            for i in np.argwhere(board != 0):
                self.update_valid_moves(i, board, valid_moves)
            return valid_moves
        else:
            for i, j in [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]:
                if 0 <= i <= 7 and 0 <= j <= 7 and board[i, j] == 0:
                    if [i, j] not in valid_moves:
                        valid_moves.append([i, j])
            if [x, y] in valid_moves:
                valid_moves.remove(move)
        
    def expand(self):
        if not self.valid_moves:
            return
        for i in self.valid_moves:
            board_cp = self.board.copy()
            row, col = i
            board_cp[row, col] = -self.player
            valid_moves_cp = self.valid_moves.copy()
            self.update_valid_moves(i, board_cp, valid_moves_cp)
            self.children.append(Node(-self.player, i, self, board_cp, valid_moves_cp))
                
    def simulation(self):
        current_player = self.player
        board_cp = self.board.copy()
        valid_moves_cp = self.valid_moves.copy()
        while valid_moves_cp:
            current_player *= -1
            x, y = random.choice(valid_moves_cp)
            board_cp[x, y] = current_player
            self.update_valid_moves([x, y], board_cp, valid_moves_cp)
            if go.IsContinuous(board_cp, [x, y]):
                winner = current_player
                self.update(winner)
                return winner
        return 0
        
    def backpropagation(self, Ni, record):
        self.Ni += Ni
        self.Wi += record[self.player]
        if self.parent:
            self.parent.backpropagation(Ni, record)
