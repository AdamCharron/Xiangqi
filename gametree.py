from pieces import *
from state_representation import *
class GameTree(object):
    '''
    Class is used to find the best move based on a game tree search with alpha beta pruning.
    It must be initialized as Gametree(gamestate,debth) where gamestate is a game object
    representing current game state and debth is the debth of the tree you wish to search in.
    It's finction is a move functions (GameTree.move()) which returns the best move as
    [row,column] (i.e. ['a',5]). The heuristic function must be externally overwritten
    If no move improves our position, it will recomend a pass returning ['pass',-1]
    '''
    def __init__ (self,gamestate,depth):
        self.current=gamestate
        self.depth=depth
    def move(self):
        '''navigate the game tree to come up with best configuration, return that gamestate'''
        possibilities=self.current.successors()
        value=float("inf")
        choice="no moves"
        if gamestate.turn:
            value=-float("inf")
        if self.current.turn:
            for child in possibilities:
                child_value=self.nodeval(child,self.depth-1,value)
                if child_value>value:
                    value=child_value
                    choice=child
        else:
            for child in possibilities:
                child_value=self.nodeval(child,self.debth-1,value)
                if child_value<value:
                    value=child_value
                    choice=child
        return choice
        #note if there is no valid moves, it will return "no moves"
    
    def nodeval(self,state,depth,parent_val):
        if depth==0:
            return state.value()
        if state.turn:
            value=-float("inf")
            possibilities=state.successors()
            if len(possibilities)==0:
                #case of no valid moves
                return state.value()
            for child in possibilities:
                child_value=self.nodeval(child,depth-1,value)
                value=max(child_value,value)
                if value>parent_val:
                    return value
        else:
            value=float("inf")
            possibilities=state.successors()
            if len(possibilities)==0:
                #case of no valid moves
                return state.value()
            for child in possibilities:
                child_value=self.nodeval(child,depth-1,value)
                value=min(child_value,value)
                if value<parent_val:
                    return value
        return value
