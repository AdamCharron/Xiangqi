from gametree import *
from pieces import *

class Gamestate(object):
    
    def __init__(self, pieces_true, pieces_false, turn, previous_piece, new_piece, eliminated=None):
        # Pieces of the true player is an array of Piece objects
        #eliminated is an optional parameter that defaults as None if not provided
        self.t_pieces = pieces_true
        
        # Defines if it is player True or False's turn,
        # Player True tries to maximize value, False minimizes value
        self.turn = turn # False Player is Black, True Player is Red
        self.f_pieces = pieces_false # Pieces held by False player
        self.move = (previous_piece, new_piece) # Original piece and new piece
        self.won = self.__pincus_winner__()# 1 if True won, -1 if False Won, 0 if no winner yet
        self.grid = self.__make_grid__()# Contains a gamegrid of the current representation
        self.eliminated=eliminated
        #print(self.grid)

        
    def successors(self):
        #successors returns all possible next gamestates from this gamestate
        successor = list()
        if self.turn:
            #print(self.grid)
            for i in range(len(self.t_pieces)):
                for (possibility, eliminate_name) in self.t_pieces[i].successors(self.grid):
                    # Shallow copy: new array with pointers to old objects
                    new_pieces = self.t_pieces[:]
                    new_pieces[i] = possibility
                    f_pieces = self.f_pieces
                    eliminated=None
                    if eliminate_name != None:
                        f_pieces = self.f_pieces[:]
                        for piece in f_pieces:
                            if piece.name == eliminate_name:
                                f_pieces.remove(piece)
                                eliminated=piece
                    successor.append(Gamestate(new_pieces, f_pieces, False, self.t_pieces[i], possibility,eliminated))
        else:
            for i in range(len(self.f_pieces)):
                for (possibility, eliminate_name) in self.f_pieces[i].successors(self.grid):
                    new_pieces = self.f_pieces[:]
                    new_pieces[i] = possibility     # Added this and next line
                    t_pieces = self.t_pieces        # Wanted to be sure, but looks like they were just forgotten
                    eliminated=None
                    if eliminate_name != None:
                        t_pieces = self.t_pieces[:]
                        for piece in t_pieces:
                            if piece.name == eliminate_name:
                                t_pieces.remove(piece)
                                eliminated=piece
                    #new_pieces[i] = possibility
                    successor.append(Gamestate(t_pieces, new_pieces, True, self.f_pieces[i], possibility,eliminated))
        return successor
    
    
    def value(self):
        #Returns the value of this gamestate (note True wishes to maximize value and False to minimizes
        #returns a value in range negative infinity to infinity
        val_T = 0
        val_F = 0
        offset = 4
        ''' self.won = 0 if no winner yet
                     = 1 if player true won
                     = -1 if player false won
        '''
        if self.won != 0:
            return self.won*float("inf")
        elif self.won == -1:
            return -float("inf")
        for piece in self.t_pieces:
            val_T += piece.get_value()
        for piece in self.f_pieces:
            val_F += piece.get_value()
        return (val_T + offset) / (val_F + offset)
        ''' The more pieces we lose, the more valuable the ones we have are.
            The more pieces the opponent loses, the more value is placed on the
            ones he has left.
            This should create a more offensive behaviour for the winning side,
            and a more defensive one for the losing side.
            
            Will test to see if this is an effective reaction method.
        '''

    
    def __make_grid__(self):
        # Makes a GameGrid matrix using all the pieces names
        # Grid is populated with 0 if that space is empty or with the name
        # of that piece if occupied
        grid=[[0]*10 for _ in range(9)]
        for piece in self.t_pieces + self.f_pieces:
            #print(piece.name)
            #print(piece.pos.x)
            #print(piece.pos.y)
            grid[piece.pos.x][piece.pos.y] = piece.name
        return grid

    
    def __pincus_winner__(self):
        # Returns 1 if player True won
        # Returns -1 if player False won
        # Returns 0 if game continues
        
        flag_True = 0
        for piece in self.t_pieces:
            #if type(piece) == General:
            if piece.name.split('.')[1].lower() == 'general':
                flag_True = 1
                break
        if flag_True == 0:
            return -1
        for piece in self.f_pieces:
            #if type(piece) == General:
            if piece.name.split('.')[1].lower() == 'general':
                return 0
        return 1
