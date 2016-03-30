from pieces import *
from initialize import *
from gametree import *
from state_representation import *

'''
Rules:
https://en.wikipedia.org/wiki/Xiangqi


Piece movements:

General (G) - can move one space orthogonally
            - cannot leave the tent
            - if it has a direct view of other general, can instantly capture it
            (wins game)

Advisor (A) - can move one spot diagonally
            - cannot leave the tent

Elephant (E) - can move 2 spaces diagonally (both spaces in same direction)
             - cannot jump over pieces (blocked if anyone diagonally adjacent)
             - cannot cross the river

Horse (H) - move one direction orthogonal, then one diagonal (away from start)
          - cannot jump over pieces (blocked if anyone orthogonally adjacent)
          - capture pieces at the end of the diagonal move

Chariot (R) - move and capture any distance orthogonally (essentially rook)
            - cannot jump over any pieces

Cannon (C) - move any distance orthogonally without jumping over any pieces
           - capture by jumping over exactly one piece in the line of fire (any
           orthogonal range, but must only have one piece ("screen") in the way)

Soldier (S) - cannot move backwards or diagonally
            - before river, can only move/capture one space forward at a time
            - after river, can move/capture one space forward/sideways
            - at end of the board, cannot move forward/backwards, but can still
            move/capture sideways

Approximate values:

Soldier before crossing the river	1
Soldier after crossing the river	2
Advisor	                                2
Elephant	                        2
Horse	                                4
Cannon	                                4.5
Chariot	                                9
(General technically count as infinite since the game ends upon its capture)


Potential Move Notation:
[piece name] ([former rank][former file])-([new rank][new file])
'''

# EMERSON: this is not to undo/undermine your code, just didn't wanna write
# over it, so copied what you had initially to lazily print off the board.
def update_board_2(total_pieces):
    ''' This function takes in a list of all the pieces as a parameter, and
        abbreviates their colours, names, and numbers before storing them all
        into a nested array game board, which is then returned.

        For example, "red.general.0" becomes "RG0".
        
        This is more or less a helper function for the print function below.
    '''
    
    board = [[0]*10 for _ in range(9)]
    for piece in total_pieces:
            tempcolour = piece.name.split('.')[0].lower()
            tempname = piece.name.split('.')[1].lower()
            tempnumber = piece.name.split('.')[2]

            # Get abbreviated colour code
            if tempcolour == "red":
                tempcolour = "R"
            elif tempcolour == "black":
                tempcolour = "B"
            else:
                raise("Invalid Colour: ")
                print(tempcolour)
                return -1

            # Get abbreviated name code
            # NOTE: Chariot is 'R' because it is pretty much a rook and 'C' was
            #       already taken by Cannon
            if tempname == "general":
                tempname = "G"
            elif tempname == "advisor":
                tempname = "A"
            elif tempname == "elephant":
                tempname = "E"
            elif tempname == "horse":
                tempname = "H"
            elif tempname == "chariot":
                tempname = "R"
            elif tempname == "cannon":
                tempname = "C"
            elif tempname == "soldier":
                tempname = "S"
            else:
                raise("Invalid Name: ")
                print(tempname)
                return -1

            # Make sure number code is valid
            if tempnumber[0] < '0' or tempnumber[0] > '4':
                raise("Invalid Number: ")
                print(tempname)
                return -1

            # Append the codes into a string for the simple name
            # Store this simple name in the board
            board[piece.pos.x][piece.pos.y] = tempcolour + tempname + tempnumber
            #print("Name: {}, abbreviated: {}".format(piece.name, board[piece.pos.x][piece.pos.y]))
    return board


def print_board_2(board):
    ''' This function takes as input the nested array of abbreviated piece
        colours, names, and numbers, and prints the game board with their
        abbreviated names, and a visual depication of the river and tent area.

        For example, starting board prints as follows:
        
        RR0    RH0    RE0   |RA0    RG0    RA1|   RE1    RH1    RR1    
        0      0      0     |0      0      0  |   0      0      0      
        0      RC0    0     |0______0______0__|   0      RC1    0      
        RS0    0      RS1    0      RS2    0      RS3    0      RS4    
        0      0      0      0      0      0      0      0      0      
        -----------------------------------------------------------
                                   river                           
        -----------------------------------------------------------
        0      0      0      0      0      0      0      0      0      
        BS0    0      BS1    0______BS2____0__    BS3    0      BS4    
        0      BC0    0     |0      0      0  |   0      BC1    0      
        0      0      0     |0      0      0  |   0      0      0      
        BR0    BH0    BE0   |BA0    BG0    BA1|   BE1    BH1    BR1  
    '''
    
    row = 0
    riverflag = False
    while row < len(board[0]):
        col = 0
        s = ''
        if row == 5 and not riverflag:
            # Print the river
            print("-"*59)
            print(" "*27 + "river" + " "*27)
            print("-"*59)
            riverflag = True
            continue
        while col < len(board):
            s += str(board[col][row])

            # Print upper and lower tent
            if (row == 2 or row == 6) and col in range (3,6):
                if str(board[col][row]) == "0":
                    s += ('__')
                if col == 5 and row == 2:
                    s += ('|   ')
                elif col == 5 and row == 6:
                    s += ('    ')
                else:
                    s += ('____')

            else:
                # Print tent sides
                if str(board[col][row]) == "0":
                    s += ('  ')
                if col == 2 and (row <= 2 or row >= 7):
                    s += ('   |')
                elif col == 5 and (row <= 2 or row >= 7):
                    s += ('|   ')
                else:
                    s += ('    ')
            col += 1
        row += 1
        print(s)
    print("\n")



def main():
    #print_board_2(update_board_2(total_pieces))


    # AI1_on and AI2_on are boolean values indicating which AI's to turn on
    # When both AI_on = False, it is human player vs human player
    # When both AI_on = True, it is AI vs AI (can set some parameters)
    # When one AI_on = True and the other is False, it is human player vs AI

    # Get the number of human players
    while True:
        number_of_human_players = input("Enter the number of human players (0, 1, or 2): ")
        if len(number_of_human_players) != 1:
            print("Invalid number of human players. There can only be 0, 1, or 2.\n")
            continue
        if number_of_human_players == '1':
            print("Beginning the game with 1 human player against an AI\n")
            AI1_on = True
            AI2_on = False
            break
        elif number_of_human_players == '2':
            print("Beginning the game with 2 human players facing off\n")
            AI1_on = False
            AI2_on = False
            break
        elif number_of_human_players == '0':
            print("Beginning the game with 2 AIs facing off\n")
            AI1_on = True
            AI2_on = True
            break
        else:
            print("Invalid number of human players. There can only be 0, 1, or 2.\n")

    #number_of_human_players = int(number_of_human_players)

    # Can set an input depth for each AI in this module, or through user input
    #input_depth1 = 5   # Arbitrary default value
    #input_depth2 = 5   # Arbitrary default value
    if AI1_on:
        while True:
            input_depth1 = input("Select the desired search depth for AI1: ")
            if len(input_depth1) != 1 or input_depth1 <= '0' or input_depth1 > '9':
                print("Invalid depth. Needs to be between 0 and 9.\n")
                continue
            break
    if AI2_on:
        while True:
            input_depth2 = input("Select the desired search depth for AI2: ")
            if len(input_depth2) != 1 or input_depth2 <= '0' or input_depth2 > '9':
                print("Invalid depth. Needs to be between 0 and 9.\n")
                continue
            break



    # WILL SEE LATER WHAT ELSE MAY NEED TO BE INPUTTED AS PARAMETERS FOR EACH AI



    # Build initial Gamestate
    # Player 1 will be Red (True), Player 2 will be Black (False)
    newgame = Gamestate(redpieces, blackpieces, True, None, None)
    #print(newgame.grid)
    print_board_2(update_board_2(newgame.t_pieces + newgame.f_pieces))
    #print(newgame.successors())

    # OK FROM THE ABOVE 3 LINES, THE FOLLOWING ISSUE OCCURRED:
    '''
    Print_board_2 line works fine which means it was probably initialized fine
    But, when i called newgame.successors(), it returned the following list:

    [['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1'],
    ['red.chariot.1', 0, 'red.cannon.1', 'red.soldier.4', 0, 0, 'black.soldier.4', 'black.cannon.1', 0, 'black.chariot.1']]

    Needless to say, this is not correct.
    The only things being called right now is the successors function from
    state_representation.
    Why are the pieces not only not where they should be in this array,
           ie: chariot and cannon are not in the same row OR column, 
    but also why is the entire thing just this same repeated row/col throughout
    the entire grid?
    '''

    # SECOND, POSSIBLY RELATED ISSUE:
    # When emerson uses his barrage of:
    #      if temp.name.strip('.')[0].lower() == .....
    # lines, in pieces.py there are errors. This is cause temp is grid[x][y]
    # Emerson treats grid as a nested array of Pieces, but the grid that Camilo
    # passes to him is a nested array of the piece's names only.
    # This causes a metric butt-fuck ton of errors in Emerson's code. 
    
    
    return

main()
