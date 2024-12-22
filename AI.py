from copy import deepcopy
import time

class frontier:
    def __init__(self):
        self.frontier = []
        
    def is_contained(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def add(self, node):
        return self.frontier.append(node)
    
class stack_frontier(frontier):    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop()
        
class quie_frontier(frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            temp = self.frontier[0]
            self.frontier = self.frontier[1:]
            return temp            

class node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
    
    def actions(self):
        possible_moves = []
        lengh = len(self.state)
        for x, list in enumerate(self.state):
            for y, num in enumerate(list):
                if num == 0:
                    row, col = x, y

        if col > 0:
            possible_moves.append("right")
        if col < lengh - 1:
            possible_moves.append("left")
        if row < lengh - 1:
            possible_moves.append("up")
        if row > 0:
            possible_moves.append("down")
        return possible_moves
        
    def print_node(self):
        print("state = ")
        for x in self.state:
            print(x)
        print(f"action = {self.action}, parent = {self.parent}, actions = {self.actions()}")
    
    def new_state(self, action):
        temp = deepcopy(self.state)
        for row, list in enumerate(temp):
            for col, num in enumerate(list):
                if num == 0:
                    if action == "right":
                        temp[row][col], temp[row][col-1] = temp[row][col-1], temp[row][col]
                        return temp
            
                    elif action == "left":
                        temp[row][col], temp[row][col+1] = temp[row][col+1], temp[row][col]
                        return temp

                    elif action == "up":
                        temp[row][col], temp[row+1][col] = temp[row+1][col], temp[row][col]
                        return temp

                    elif action == "down":
                        temp[row][col], temp[row-1][col] = temp[row-1][col], temp[row][col]        
                        return temp
            
        
def solve(da, algoritm, goal):
    
    frontier = algoritm()
    frontier.add(da)
    explored = []

    while True:
        if frontier.empty():
            raise Exception("no solution")

        da = frontier.remove()

        if da.state == goal:
            action = []
            states = []
            while da.parent != None:
                action.append(da.action)
                states.append(da.state)
                da = da.parent
            return action
        
        explored.append(da.state)
        for command in da.actions():
            state = da.new_state(command)
            if state not in explored:
                if state not in frontier.frontier:
                    neighbor = node(state, da, command)
                    frontier.add(neighbor)

temp_state = [[1,2,3], [4,5,6],[7,8,0]]  
temp_node = node([[4, 2, 3], [6, 0, 1], [7, 5, 8]] ,None,None)
a = time.time()
print(solve(temp_node,stack_frontier,temp_state))
b = time.time()
print(b-a)