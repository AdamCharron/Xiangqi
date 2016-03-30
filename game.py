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


def update_board_from_pieces(total_pieces):
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



def update_board_from_grid(grid):
    ''' This function takes in a the existing grid as a parameter, and
        abbreviates all pieces' colours, names, and numbers before storing them
        into a nested array game board, which is then returned.

        For example, "red.general.0" becomes "RG0".
        
        This is more or less a helper function for the print function below.
    '''
    
    board = [[0]*10 for _ in range(9)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            piece = str(grid[i][j])
            if piece != '0':
                tempcolour = piece.split('.')[0].lower()
                tempname = piece.split('.')[1].lower()
                tempnumber = piece.split('.')[2]

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
                board[i][j] = tempcolour + tempname + tempnumber
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
    #print("\n")



def main():
    #print_board_2(update_board_2(total_pieces))


    # AI1_on and AI2_on are boolean values indicating which AI's to turn on
    # When both AI_on = False, it is human player vs human player
    # When both AI_on = True, it is AI vs AI (can set some parameters)
    # When one AI_on = True and the other is False, it is human player vs AI

    # Get the number of human players
    sarcastic_count = 0
    while True:
        sarcastic_count += 1
        if sarcastic_count > 7:
            print("...Really? -_- Just type '0', '1', or '2'. Jesus Christ.\n")
        elif sarcastic_count > 3:
            print("Come on. This is not hard. You're better than this.\n")
            
        
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

    # Can set an input depth for each AI in this module, or through user input
    input_depth1 = 5   # Arbitrary default value
    input_depth2 = 5   # Arbitrary default value
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
    current_state = Gamestate(redpieces, blackpieces, True, None, None)
    #print_board_2(update_board_from_pieces(newgame.t_pieces + newgame.f_pieces))
    #print_board_2(update_board_from_grid(newgame.grid))

    game_over = False
    while not game_over:

        if current_state.turn:
            if AI1_on:
                # Deal with AI and such as
                print("7")
            else:
                # Player move
                while True:
                    input_move = str(input("\nPlayer 1's move. Please enter the piece name and next location. Type \"help\" for help, type \"print\" to print the game board: "))
                    if input_move == "help":
                        print("\n------------------------------------- HELP -------------------------------------\nThe move should be of the following form:\n\t- 3 char piece code: [colour][piece name][piece number]\n\t- Tuple location to move that piece (x,y)\n\t(Same line, separated by a space)\n\nThe colour is either 'R' or 'B' for each player\n\nThe piece names are as follows:\n\t- G = general\n\t- A = advisor\n\t- E = elephant\n\t- H = horse\n\t- R = chariot\n\t- C = cannon\n\t- S = soldier\n\nPiece number is the number of that piece from each type (see grid)\n\nThe position to which this piece moves will be inputted as a set of coordinates in the form \"(x,y)\".\nIt should be noted that the board's origin is at the bottom left corner, and it the baord dimensions are 10x9\nIndexing begins at 0, so the point (3,2) corresponds to the 4th column and 3rd row of the grid\n\nThe grid can be printed by typing \"print\" \n\nAn example of a piece movement from initial state is: \"RA0  (4,1)\"\n--------------------------------------------------------------------------------\n")
                    elif input_move == "print":
                        print("\n------------------------------------- PRINT ------------------------------------\n")
                        print_board_2(update_board_from_grid(current_state.grid))
                        print("\n--------------------------------------------------------------------------------\n")
                    else:
                        move_setup = input_move.split(" ")
                        if len(move_setup) != 2:
                            print("Invalid length of input string. Try again.\n")
                            continue
                        if len(move_setup[0]) != 3:
                            print("Invalid length of piece code string. Try again.\n")
                            continue
                        if len(move_setup[1]) != 5:
                            print("Invalid length of coordinate string. Try again.\n")
                            continue

                        if move_setup[1][0] != "(" or move_setup[1][4] != ")" or move_setup[1][2] != ",":
                            print("Invalid coordinate input format. Try again. Type \"help\" for help.")
                        
                        tempcolour = move_setup[0][0].upper()
                        tempname = move_setup[0][1].upper()
                        tempnumber = str(move_setup[0][2])
                        tempx = str(move_setup[1][1])
                        tempy = str(move_setup[1][3])
                        piecename = ""
                        coord = [-1, -1]

                        # Verify colour code
                        if tempcolour == "B":
                            if current_state.turn:
                                print("Cannot move an opponent's pieces.")
                                continue
                            piecename += "black."
                        elif tempcolour == "R":
                            if not current_state.turn:
                                print("Cannot move an opponent's pieces.")
                                continue
                            piecename += "red."
                        else:
                            print("Invalid colour code. Must be 'R' or 'B'")
                            continue

                        # Verfiy piece name and piece number
                        if tempname == "G":
                            piecename += "general."
                            if tempnumber != "0":
                                print("Invalid piece number. Must be 0 for general. Type \"print\" to print game board")
                                continue
                        elif tempname == "A":
                            piecename += "advisor."
                            if tempnumber not in ["0", "1"]:
                                print("Invalid piece number. Must be 0 or 1 for advisor. Type \"print\" to print game board")
                                continue
                        elif tempname == "E":
                            piecename += "elephant."
                            if tempnumber not in ["0", "1"]:
                                print("Invalid piece number. Must be 0 or 1 for elephant. Type \"print\" to print game board")
                                continue
                        elif tempname == "H":
                            piecename += "horse."
                            if tempnumber not in ["0", "1"]:
                                print("Invalid piece number. Must be 0 or 1 for horse. Type \"print\" to print game board")
                                continue
                        elif tempname == "R":
                            piecename += "chariot."
                            if tempnumber not in ["0", "1"]:
                                print("Invalid piece number. Must be 0 or 1 for chariot. Type \"print\" to print game board")
                                continue
                        elif tempname == "C":
                            piecename += "cannon."
                            if tempnumber not in ["0", "1"]:
                                print("Invalid piece number. Must be 0 or 1 for cannon. Type \"print\" to print game board")
                                continue
                        elif tempname == "S":
                            piecename += "soldier."
                            if tempnumber not in ["0", "1", "2", "3", "4"]:
                                print("Invalid piece number. Must be 0, 1, 2, 3, or 4 for soldier. Type \"print\" to print game board")
                                continue
                        else:
                            print("Invalid piece name. Type \"help\" for help.")
                            continue
                        piecename += tempnumber

                        # Verify coordinate
                        if tempx >= "0" and tempx <= "9":
                            coord[0] = int(tempx)
                        else:
                            print("Invalid x coordinate. Must be from 0 to 9")
                            continue

                        if tempy >= "0" and tempy <= "8":
                            coord[1] = int(tempy)
                        else:
                            print("Invalid y coordinate. Must be from 0 to 8")
                            continue
                        coord = tuple(coord)

                        # Now find the piece, and make sure this is a valid move
                        validMoveFlag = False
                        nextpiece = None
                        for piece in total_pieces:
                            if piece.name == piecename:
                                for newpiece in piece.successors(current_state.grid):
                                    if coord == Position(newpiece[0]):
                                        validMoveFlag = True
                                        nextpiece = newpiece[0]
                                        break
                                if validMoveFlag:
                                    break
                        if not validMoveFlag:
                            print("Invalid move for this piece.")
                            continue
                        
                            
        else:
            if AI2_on:
                # Deal with AI and such as
                print("7")
            else:
                # Player move
                print("8")
        current_state.turn = not current_state.turn     # Alternate turns
        if current_state.won != 0:
            # someone won. Yay. deal with it.
            game_over = True
    
    return

main()
