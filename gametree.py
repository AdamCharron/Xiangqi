from pieces import *
from state_representation import *

class GameTree(object):
    '''
    Class is used to find the best move based on a game tree search with
    alpha beta pruning. It must be initialized as Gametree(gamestate,debth)
    where gamestate is a game object representing current game state and debth
    is the debth of the tree you wish to search in. It's finction is a move
    functions (GameTree.move()) which returns the best move as [row,column]
    (i.e. ['a',5]). The heuristic function must be externally overwritten.

    If no move improves our position, it will recomend a pass returning
    ['pass',-1]
    '''

    def __init__ (self, gamestate, depth):
        self.current = gamestate
        self.depth = depth
        # Maximum depth of the tree search.
        # Increase for better AI, decrease for time improvement
        

    def move(self):
        '''navigate the game tree to come up with best configuration,
        return that gamestate'''
        
        possibilities = min_order(self.current)
        if len(possibilities) == 0:
            #case of no valid moves
            return self.current.value()
        
        value = float("inf")
        choice = "no moves"
        if gamestate.turn:
            value = -float("inf")
        if self.current.turn:
            for child in possibilities:
                child_value = self.nodeval(child, self.depth-1, value)
                if child_value > value:
                    value = child_value
                    choice = child
        else:
            for child in possibilities:
                child_value = self.nodeval(child, self.debth-1, value)
                if child_value < value:
                    value = child_value
                    choice = child
        return choice
        #note if there is no valid moves, it will return the string "no moves", otherwise it returns the best gamestate

    
    def nodeval(self, state, depth, parent_val):
        #evaluates the value of chosing each child in the gametree by considering up to debth nodes beneath it.
        if depth == 0:
            return state.value()
        
        possibilities = min_order(state)
        if len(possibilities) == 0:
            #case of no valid moves
            return state.value()
        
        if state.turn:
            value = -float("inf")
            for child in possibilities:
                child_value = self.nodeval(child, depth-1, value)
                value = max(child_value, value)
                if value > parent_val:
                    return value
        else:
            value = float("inf")
            for child in possibilities:
                child_value = self.nodeval(child, depth-1, value)
                value = min(child_value, value)
                if value < parent_val:
                    return value
        return value

    
    def min_order(self,state):
        minmax = not state.turn
        return mergeSort(state.successors(), minmax)

    
    def mergeSort(self, alist, minmax):
        #if minmax is True, it is smallest to largest. Otherwise it is largest to smallest
        if minmax
            if len(alist) > 1:
                mid = len(alist) // 2
                lefthalf = alist[:mid]
                righthalf = alist[mid:]
                self.mergeSort(lefthalf)
                self.mergeSort(righthalf)
                i=0
                j=0
                k=0
                while i < len(lefthalf) and j < len(righthalf):
                    if lefthalf[i].value() < righthalf[j].value():
                        alist[k] = lefthalf[i]
                        i = i + 1
                    else:
                        alist[k] = righthalf[j]
                        j = j + 1
                    k = k + 1
    
                while i < len(lefthalf):
                    alist[k] = lefthalf[i]
                    i = i + 1
                    k = k + 1
    
                while j < len(righthalf):
                    alist[k] = righthalf[j]
                    j = j + 1
                    k = k + 1
            return alist
        else:
            if len(alist) > 1:
                mid = len(alist) // 2
                lefthalf = alist[:mid]
                righthalf = alist[mid:]
                mergeSort(lefthalf)
                mergeSort(righthalf)
                i=0
                j=0
                k=0
                while i < len(lefthalf) and j < len(righthalf):
                    if lefthalf[i].value > righthalf[j].value:
                        alist[k] = lefthalf[i]
                        i = i + 1
                    else:
                        alist[k] = righthalf[j]
                        j = j + 1
                    k = k + 1
    
                while i < len(lefthalf):
                    alist[k] = lefthalf[i]
                    i = i + 1
                    k = k + 1
    
                while j < len(righthalf):
                    alist[k] = righthalf[j]
                    j = j + 1
                    k = k + 1
            return alist
