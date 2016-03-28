from abc import ABCMeta, abstractmethod
from gametree import *

class Position(object):
    def __init__(self,x,y):
        '''Origin at bottom left of board
           Red at bottom, Black at top
           Red is True, Black is False'''
        self.x = x
        self.y = y

    def get_pos(self):
        return (self.x,self.y)

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

class Piece(object):
    __metaclass__ = ABCMeta

    def __init__(self, position, color, name):
        '''Red = True
           Black = False'''
        self.pos = position
        self.color = color
        self.value = 0
        self.name=name
        #name is the distinguishing characteristic of one piece
        #all pieces must have a unique name and moving a piece
        #does not change its name
        #name format [color].[piece].[number]

    @abstractmethod
    def successors(self, grid):
        '''Return list of tuples (piece,eliminate) where piece is the
        new piece object after moving and eliminate is the piece name
        that gets removed as a result of the move
        '''
        return NotImplemented

    def get_value(self):
        return self.value

    def get_pos(self):
        return self.pos.get_pos()

    def check(self, pos, grid):
        if pos[0] < 0 or pos[0] >= 9 or pos[1] < 0 or pos[1] >= 10:
            return (False,None)

        potential = grid[pos[0]][pos[1]]

        if not potential: # Empty
            return (True,None)

        if self.color: # Red
            if potential.split('.')[0].lower() == 'red':
                return (False,None)
            else:
                return (True,potential) # Will kill a piece
        else: # Black
            if potential.split('.')[0].lower() == 'black':
                return (False,None)
            else:
                return (True,potential) # Will kill a piece

        raise("Should never get here")
        return (False,None)


class General(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 0

    def successors(self, grid):
        ret_pieces = []
        if self.color: # Red
            # tent from x={3,5}, y={0,2}
            if self.get_pos() == (3,0):
                possibilities = [(3,1),(4,0)]
            elif self.get_pos() == (4,0):
                possibilities = [(3,0),(4,1),(5,0)]
            elif self.get_pos() == (5,0):
                possibilities = [(4,0),(5,1)]
            elif self.get_pos() == (3,1):
                possibilities = [(3,0),(4,1),(3,2)]
            elif self.get_pos() == (4,1):
                possibilities = [(4,0),(3,1),(5,1),(4,2)]
            elif self.get_pos() == (5,1):
                possibilities = [(5,0),(4,1),(5,2)]
            elif self.get_pos() == (3,2):
                possibilities = [(3,1),(4,2)]
            elif self.get_pos() == (4,2):
                possibilities = [(3,2),(4,1),(5,2)]
            elif self.get_pos() == (5,2):
                possibilities = [(4,2),(5,1)]
            else:
                raise("Red general not in palace!")
            for i in range(self.pos.y+1,10):
                piece = grid[self.pos.x][i]
                if piece:
                    if piece.split('.')[0].lower() == 'black' and piece.split('.')[1].lower() == 'general':
                        possibilities.append([(self.pos.x,i)]) # Flying general
                    break
        else:
            # black general, tent from x={3,5}, y={7,9}
            if self.get_pos() == (3,9):
                possibilities = [(3,8),(4,9)]
            elif self.get_pos() == (4,9):
                possibilities = [(3,9),(4,8),(5,9)]
            elif self.get_pos() == (5,9):
                possibilities = [(4,9),(5,8)]
            elif self.get_pos() == (3,8):
                possibilities = [(3,9),(4,8),(3,7)]
            elif self.get_pos() == (4,8):
                possibilities = [(4,9),(3,8),(5,8),(4,7)]
            elif self.get_pos() == (5,8):
                possibilities = [(5,9),(4,8),(5,7)]
            elif self.get_pos() == (3,7):
                possibilities = [(3,8),(4,7)]
            elif self.get_pos() == (4,7):
                possibilities = [(3,7),(4,8),(5,7)]
            elif self.get_pos() == (5,7):
                possibilities = [(4,7),(5,8)]
            else:
                raise("Black general not in palace!")
            for i in range(self.pos.y-1,-1,-1):
                piece = grid[self.pos.x][i]
                if piece:
                    if piece.split('.')[0].lower() == 'red' and piece.split('.')[1].lower() == 'general':
                        possibilities.append([(self.pos.x,i)]) # Flying general
                    break

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (General(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Advisor(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 2

    def successors(self, grid):
        ret_pieces = []
        if self.color: # Red
            # tent from x={3,5}, y={0,2}
            if self.get_pos() == (3,0):
                possibilities = [(4,1)]
            elif self.get_pos() == (5,0):
                possibilities = [(4,1)]
            elif self.get_pos() == (4,1):
                possibilities = [(3,0),(5,0),(3,2),(5,2)]
            elif self.get_pos() == (3,2):
                possibilities = [(4,1)]
            elif self.get_pos() == (5,2):
                possibilities = [(4,1)]
            else:
                raise("Red advisor not in palace!")
        else:
            # black general, tent from x={3,5}, y={7,9}
            if self.get_pos() == (3,9):
                possibilities = [(4,8)]
            elif self.get_pos() == (5,9):
                possibilities = [(4,8)]
            elif self.get_pos() == (4,8):
                possibilities = [(3,9),(5,9),(3,7),(5,7)]
            elif self.get_pos() == (3,7):
                possibilities = [(4,8)]
            elif self.get_pos() == (5,7):
                possibilities = [(4,8)]
            else:
                raise("Black advisor not in palace!")

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (Advisor(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Elephant(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 2

    def successors(self, grid):
        ret_pieces = []
        possibilities = []
        if self.color: # Red
            # tent from x={3,5}, y={0,2}
            if self.get_pos() == (2,0):
                if not grid[3][1]:
                    possibilities.append((4,2))
                if not grid[1][1]:
                    possibilities.append((0,2))
            elif self.get_pos() == (0,2):
                if not grid[1][3]:
                    possibilities.append((2,4))
                if not grid[1][1]:
                    possibilities.append((2,0))
            elif self.get_pos() == (2,4):
                if not grid[1][3]:
                    possibilities.append((0,2))
                if not grid[3][3]:
                    possibilities.append((4,2))
            elif self.get_pos() == (6,0):
                if not grid[5][1]:
                    possibilities.append((4,2))
                if not grid[7][1]:
                    possibilities.append((8,2))
            elif self.get_pos() == (8,2):
                if not grid[7][3]:
                    possibilities.append((6,4))
                if not grid[7][1]:
                    possibilities.append((6,0))
            elif self.get_pos() == (6,4):
                if not grid[7][3]:
                    possibilities.append((8,2))
                if not grid[5][3]:
                    possibilities.append((4,2))
            elif self.get_pos() == (4,2):
                if not grid[3][1]:
                    possibilities.append((2,0))
                if not grid[3][3]:
                    possibilities.append((2,4))
                if not grid[5][3]:
                    possibilities.append((6,4))
                if not grid[5][1]:
                    possibilities.append((6,0))
            else:
                raise("Impossible Red Elephant position")
        else:
            # black general, tent from x={3,5}, y={7,9}
            if self.get_pos() == (2,9):
                if not grid[3][8]:
                    possibilities.append((4,7))
                if not grid[1][8]:
                    possibilities.append((0,7))
            elif self.get_pos() == (0,7):
                if not grid[1][6]:
                    possibilities.append((2,5))
                if not grid[1][8]:
                    possibilities.append((2,9))
            elif self.get_pos() == (2,5):
                if not grid[1][6]:
                    possibilities.append((0,7))
                if not grid[3][6]:
                    possibilities.append((4,7))
            elif self.get_pos() == (6,9):
                if not grid[5][8]:
                    possibilities.append((4,7))
                if not grid[7][8]:
                    possibilities.append((8,7))
            elif self.get_pos() == (8,7):
                if not grid[7][6]:
                    possibilities.append((6,5))
                if not grid[7][8]:
                    possibilities.append((6,9))
            elif self.get_pos() == (6,5):
                if not grid[7][6]:
                    possibilities.append((8,7))
                if not grid[5][6]:
                    possibilities.append((4,7))
            elif self.get_pos() == (4,7):
                if not grid[3][8]:
                    possibilities.append((2,9))
                if not grid[3][6]:
                    possibilities.append((2,5))
                if not grid[5][6]:
                    possibilities.append((6,5))
                if not grid[5][8]:
                    possibilities.append((6,9))
            else:
                raise("Impossible Black Elephant Position")

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (Elephant(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Horse(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 4

    def successors(self, grid):
        ret_pieces = []
        possibilities = []

        if self.pos.x > 1: # Left
            if not grid[self.pos.x-1][self.pos.y]: # check left hobble
                possibilities.extend( [(self.pos.x-2,self.pos.y-1),(self.pos.x-2,self.pos.y+1)] )
        if self.pos.x < 7: # Right
            if not grid[self.pos.x+1][self.pos.y]: # check right hobble
                possibilities.extend( [(self.pos.x+2,self.pos.y-1),(self.pos.x+2,self.pos.y+1)] )
        if self.pos.y > 1: # Down
            if not grid[self.pos.x][self.pos.y-1]: # check down hobble
                possibilities.extend( [(self.pos.x-1,self.pos.y-2),(self.pos.x+1,self.pos.y-2)] )
        if self.pos.y < 8: # Up
            if not grid[self.pos.x][self.pos.y+1]: # check up hobble
                possibilities.extend( [(self.pos.x-1,self.pos.y+2),(self.pos.x+1,self.pos.y+2)] )

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (Horse(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Chariot(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 9

    def successors(self, grid):
        ret_pieces = []
        possibilities = []
        
        for i in range(self.pos.x+1,9): # Right
            temp = grid[i][self.pos.y]
            if not temp:
                possibilities.append( (i,self.pos.y) )
            else:
                if self.color:
                    if temp.name.strip('.')[0].lower() == 'black':
                        possibilities.append( (i,self.pos.y) )
                else:
                    if temp.name.strip('.')[0].lower() == 'red':
                        possibilities.append( (i,self.pos.y) )
                break

        for i in range(self.pos.x-1,-1,-1): # Left
            temp = grid[i][self.pos.y]
            if not temp:
                possibilities.append( (i,self.pos.y) )
            else:
                if self.color:
                    if temp.name.strip('.')[0].lower() == 'black':
                        possibilities.append( (i,self.pos.y) )
                else:
                    if temp.name.strip('.')[0].lower() == 'red':
                        possibilities.append( (i,self.pos.y) )
                break

        for j in range(self.pos.y+1,10): # Up
            temp = grid[self.pos.x][j]
            if not temp:
                possibilities.append( (self.pos.x,j) )
            else:
                if self.color:
                    if temp.name.strip('.')[0].lower() == 'black':
                        possibilities.append( (self.pos.x,j) )
                else:
                    if temp.name.strip('.')[0].lower() == 'red':
                        possibilities.append( (self.pos.x,j) )
                break

        for j in range(self.pos.y-1,-1,-1): # Down
            temp = grid[self.pos.x][j]
            if not temp:
                possibilities.append( (self.pos.x,j) )
            else:
                if self.color:
                    if temp.name.strip('.')[0].lower() == 'black':
                        possibilities.append( (self.pos.x,j) )
                else:
                    if temp.name.strip('.')[0].lower() == 'red':
                        possibilities.append( (self.pos.x,j) )
                break

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (Chariot(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Cannon(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)
        self.value = 4.5

    def successors(self, grid):
        ret_pieces = []
        move_poss = []
        attack_poss = []
        
        count = 0
        for i in range(self.pos.x+1,9): # Right
            temp = grid[i][self.pos.y]
            if not temp:
                if not count:
                    move_poss.append( (i,self.pos.y) ) # Can move
                else:
                    continue
            else:
                if not count:
                    count += 1 # Found a piece to jump over
                    continue
                else:
                    if self.color:
                        if temp.name.strip('.')[0].lower() == 'black':
                            attack_poss.append( (i,self.pos.y) )
                    else:
                        if temp.name.strip('.')[0].lower() == 'red':
                            attack_poss.append( (i,self.pos.y) )
                    break

        count = 0
        for i in range(self.pos.x-1,-1,-1): # Left
            temp = grid[i][self.pos.y]
            if not temp:
                if not count:
                    move_poss.append( (i,self.pos.y) ) # Can move
                else:
                    continue
            else:
                if not count:
                    count += 1 # Found a piece to jump over
                    continue
                else:
                    if self.color:
                        if temp.name.strip('.')[0].lower() == 'black':
                            attack_poss.append( (i,self.pos.y) )
                    else:
                        if temp.name.strip('.')[0].lower() == 'red':
                            attack_poss.append( (i,self.pos.y) )
                    break

        count = 0
        for j in range(self.pos.y+1,10): # Up
            temp = grid[self.pos.x][j]
            if not temp:
                if not count:
                    move_poss.append( (self.pos.x,j) ) # Can move
                else:
                    continue
            else:
                if not count:
                    count += 1 # Found a piece to jump over
                    continue
                else:
                    if self.color:
                        if temp.name.strip('.')[0].lower() == 'black':
                            attack_poss.append( (self.pos.x,j) )
                    else:
                        if temp.name.strip('.')[0].lower() == 'red':
                            attack_poss.append( (self.pos.x,j) )
                    break

        count = 0
        for j in range(self.pos.y-1,-1,-1): # Down
            temp = grid[self.pos.x][j]
            if not temp:
                if not count:
                    move_poss.append( (self.pos.x,j) ) # Can move
                else:
                    continue
            else:
                if not count:
                    count += 1 # Found a piece to jump over
                    continue
                else:
                    if self.color:
                        if temp.name.strip('.')[0].lower() == 'black':
                            attack_poss.append( (self.pos.x,j) )
                    else:
                        if temp.name.strip('.')[0].lower() == 'red':
                            attack_poss.append( (self.pos.x,j) )
                    break

        for poss in move_poss:
            retval = self.check(poss, grid)
            if retval[0] and not retval[1]: # Didn't land on anything
                ret_pieces.append( (Cannon(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        for poss in attack_poss:
            retval = self.check(poss, grid)
            if retval[0] and retval[1]: # Killed something
                ret_pieces.append( (Cannon(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

class Soldier(Piece):
    def __init__(self, position, color, name):
        super().__init__(position,color,name)

    def _across_river(self):
        if (self.pos.y>4 and self.color) or (self.pos.y<5 and not self.color):
            return True # Soldier has crossed river
        else:
            return False # Solder has not crossed river

    def successors(self, grid):
        ret_pieces = []
        
        if self._across_river():
            if self.color:
                possibilities = [(self.pos.x,self.pos.y+1),(self.pos.x-1,self.pos.y),(self.pos.x+1,self.pos.y)]
            else:
                possibilities = [(self.pos.x,self.pos.y-1),(self.pos.x-1,self.pos.y),(self.pos.x+1,self.pos.y)]
        else:
            if self.color:
                possibilities = [(self.pos.x,self.pos.y+1)]
            else:
                possibilities = [(self.pos.x,self.pos.y-1)]

        for possibility in possibilities:
            retval = self.check(possibility, grid)
            if retval[0]:
                ret_pieces.append( (Soldier(Position(possibility[0],possibility[1]),self.color,self.name) , retval[1]) )

        return ret_pieces

    def get_value(self):
        if self._across_river():
            return 2 # Soldier has crossed river
        else:
            return 1 # Solder has not crossed river
