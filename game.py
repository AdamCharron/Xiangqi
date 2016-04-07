from pieces import *
from initialize import *
from gametree import *
from state_representation import *

'''
Rules:
https://en.wikipedia.org/wiki/Xiangqi
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
    return board


def print_board_2(board):
    ''' This function takes as input the nested array of abbreviated piece
        colours, names, and numbers, and prints the game board with their
        abbreviated names, and a visual depication of the river and tent area.

        For example, starting board prints as follows:
        
0      RR0    RH0    RE0   |RA0    RG0    RA1|   RE1    RH1    RR1    
1      0      0      0     |0      0      0  |   0      0      0      
2      0      RC0    0     |0______0______0__|   0      RC1    0      
3      RS0    0      RS1    0      RS2    0      RS3    0      RS4    
4      0      0      0      0      0      0      0      0      0      
      -----------------------------------------------------------
                                 river                           
      -----------------------------------------------------------
5      0      0      0      0      0      0      0      0      0      
6      BS0    0      BS1    0______BS2____0__    BS3    0      BS4    
7      0      BC0    0     |0      0      0  |   0      BC1    0      
8      0      0      0     |0      0      0  |   0      0      0      
9      BR0    BH0    BE0   |BA0    BG0    BA1|   BE1    BH1    BR1    

       A      B      C      D      E      F      G      H      I
       
    '''
    
    row = 0
    riverflag = False
    while row < len(board[0]):
        col = 0
        if row == 5 and not riverflag:
            # Print the river
            print("      " + "-"*59)
            print("      " + " "*27 + "river" + " "*27)
            print("      " + "-"*59)
            riverflag = True
            continue
        s = str(row) + "      "
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
    s = '\n       '
    print("\n       A      B      C      D      E      F      G      H      I")
    print("\n")


def print_help():
    ''' Helper function for printing the help table. No parameters or return.'''
    
    print("\n\n------------------------------------ HELP -------------------------------------- ")
    print("A move is made by a user input of the form:\n\t- 3 character piece code\n\t- Coordinates of the position where that piece will move\n\t(these two arguments are on the same line, separated by a space)\n")
    print("The character code is of the following form: [player colour][piece name letter][piece number]\n")
    print("The player colour is either 'R' for red, or 'B' for black.\nA player can only move his/her own pieces.\n")
    print("The piece name letter is a letter corresponding to the piece type:\n\tG = general\n\tA = advisor\n\tE = elephant\n\tH = horse\n\tR = chariot\n\tC = cannon\n\tS = soldier\n")
    print("The piece number corresponds to the piece type that the player wishes to move.\n\n")
    print("The coordinates for this piece's destination must be inputed in the form XY where X is the letter corresponding to the column, and Y is the number corresponding to the row.\nIn this board, x ranges from A to I, and y from 0 to 9 (origin is at the top left)\n")
    print("Inputs are not case sensitive.\n")
    print("A player can end the game by typing \"end\".\n")
    print("An example of a valid input would be: RA1 E1\nThis would move red admiral 1 to the spot E1 on the board.\n")
    print("--------------------------------------------------------------------------------\n\n")
    return


def print_rules():
    print("\n\n----------------------------------- RULES -------------------------------------- ")
    print("The objective of the game is to capture the opponent's general. Whoever does so wins the game.\n")
    print("There is a river horizontally across the middle of the board that can be crossed by anyone except the Advisors, the Elephants, and the Generals (with the exception of the \"flying general\" move described below).\n")
    print("There are two 3x3 tents, one for each player, centered at the top and bottom of the board. The Advisors cannot leave the tent, and the Generals can only leave the tent for the the \"flying general\" move described below. Any other piece from either player can enter or leave either tent.\n")
    print("General (G)\nCan move and capture one space orthogonally, but cannot leave the tent. If it has a direct view of the other general, it can instantly capture it via the \"flying general\" move to win the game.\n")
    print("Advisor (A)\nCan move and capture one spot diagonally, but cannot leave the tent.\n")
    print("Elephant (E)\nCan move and capture 2 spaces diagonally (both spaces in same direction), cannot jump over pieces (blocked if anyone is one spot diagonally adjacent). It also cannot cross the river.\n")
    print("Horse (H)\nCan move one direction orthogonally, then one diagonally (away from where it started). It cannot jump over pieces (blocked if anyone orthogonally adjacent), but can capture pieces at the end of the diagonal move.\n")
    print("Chariot (R)\nMuch like a rook in chess, it can move and capture any distance orthogonally but cannot jump over any pieces.\n")
    print("Cannon (C)\nCan move any distance orthogonally without jumping over any pieces. It can capture any distance orthogonally by jumping over exactly one piece in the line of fire (any orthogonal range, but must only have one piece (\"screen\") in the way).\n")
    print("Soldier (S)\nCannot move backwards or diagonally before river, can only move/capture one space forward at a time. After the river, it can move/capture one space forward/sideways. At end of the board, it cannot move forward/backwards, but can still move/capture sideways.\n")
    print("--------------------------------------------------------------------------------\n\n")
    return


def format_input(input_str, turn):
    ''' Takes turn and input string as parameters.
    Formats formats the input string into the proper piece name and
    destination coordinate. Also catches improper inputs and prints the
    reason for the improper input, then returns -1, -1.

    Expect input of the form "RA1 E1" (not case sensitive)
    If successful, this function returns piecename and the coordinate as a list.
    '''

    input_str = input_str.split(" ")
    if len(input_str) != 2:
        print("\nIncorrect number of input arguments.")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1

    if len(input_str[0]) != 3:
        print("\nIncorrect piece code length.")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1

    if len(input_str[1]) != 2:
        print("\nIncorrect coordinate input length.")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1

    # The lengths are good, now checking for valid input and building piecename
    tempcolour = input_str[0][0].upper()
    tempname = input_str[0][1].upper()
    tempnumber = str(input_str[0][2])
    tempx = str(input_str[1][0])
    tempy = str(input_str[1][1])
    piecename = ""
    coord = []


    # Colour
    if tempcolour == "R":
        if not turn:
            print("\nCannot move opponent's pieces.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += "red."
    elif tempcolour == "B":
        if turn:
            print("\nCannot move opponent's pieces.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += "black."
    else:
        print("\nInvalid piece colour.")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1


    # Piece name letter and number
    if tempname == "G":
        piecename += "general."
        if tempnumber != "0":
            print("\nInvalid piece number. The general can only have number 0.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "A":
        piecename += "advisor."
        if tempnumber not in ["0", "1"]:
            print("\nInvalid piece number. The advisor can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "E":
        piecename += "elephant."
        if tempnumber not in ["0", "1"]:
            print("\nInvalid piece number. The elephant can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "H":
        piecename += "horse."
        if tempnumber not in ["0", "1"]:
            print("\nInvalid piece number. The horse can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "R":
        piecename += "chariot."
        if tempnumber not in ["0", "1"]:
            print("\nInvalid piece number. The chariot can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "C":
        piecename += "cannon."
        if tempnumber not in ["0", "1"]:
            print("\nInvalid piece number. The cannon can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "S":
        piecename += "soldier."
        if tempnumber not in ["0", "1", "2", "3", "4"]:
            print("\nInvalid piece number. The soldier can only have numbers 0, 1, 2, 3, or 4.")
            print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
            return -1, -1
        piecename += tempnumber
        
    else:
        print("\nInvalid piece name letter.")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1


    # If we got here, the piecename is valid. Now we handle the coordinates
    if tempx == "A" or tempx == "a":
        tempx = 0
    elif tempx == "B" or tempx == "b":
        tempx = 1
    elif tempx == "C" or tempx == "c":
        tempx = 2
    elif tempx == "D" or tempx == "d":
        tempx = 3
    elif tempx == "E" or tempx == "e":
        tempx = 4
    elif tempx == "F" or tempx == "f":
        tempx = 5
    elif tempx == "G" or tempx == "g":
        tempx = 6
    elif tempx == "H" or tempx == "h":
        tempx = 7
    elif tempx == "I" or tempx == "i":
        tempx = 8
    else:
        print("\nInvalid x coordinate. x coordinates should be between 0 and 8")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1
    if tempy not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print("\nInvalid y coordinate. y coordinates should be between 0 and 9")
        print("Try again. Type \"help\" for help if needed, and type \"rules\" for rules.\n")
        return -1, -1
    coord = [tempx, int(tempy)]
    
    return [piecename, coord]


def player_move(piecename, coords, current_state):
    ''' Takes as input the piecename and coords determined in format_input for
    the piece being moved, as well as the current state of the game.
    Will check if the move is possible.
    If so it will return the gamestate after this move has been made.
    If not it will return None.
    '''

    if current_state.turn:
        for piece in current_state.t_pieces:
            if piece.name == piecename:
                eliminated = None
                for successor in piece.successors(current_state.grid):
                    if Position(coords[0], coords[1]) == successor[0].pos:
                        F = current_state.f_pieces[:]
                        if successor[1]:  # Eliminate an opponent's piece
                            for elim_piece in current_state.f_pieces:
                                if elim_piece.name == successor[1]:
                                    F.remove(elim_piece)
                                    eliminated = elim_piece
                                    break                
                        newpiece = successor[0]
                        T = current_state.t_pieces[:]
                        T.remove(piece)
                        T.append(newpiece)
                        return Gamestate(T, F, not current_state.turn, piece, newpiece, eliminated)
        return None

    else:
        for piece in current_state.f_pieces:
            if piece.name == piecename:
                eliminated = None
                for successor in piece.successors(current_state.grid):
                    if Position(coords[0], coords[1]) == successor[0].pos:
                        T = current_state.t_pieces[:]
                        if successor[1]:  # Eliminate an opponent's piece
                            for elim_piece in current_state.t_pieces:
                                if elim_piece.name == successor[1]:
                                    T.remove(elim_piece)
                                    eliminated = elim_piece
                                    break                
                        newpiece = successor[0]
                        F = current_state.f_pieces[:]
                        F.remove(piece)
                        F.append(newpiece)
                        return Gamestate(T, F, not current_state.turn, piece, newpiece, eliminated)
        return None


def num_to_letter(num):
    if num == 0:
        return "A"
    elif num == 1:
        return "B"
    elif num == 2:
        return "C"
    elif num == 3:
        return "D"
    elif num == 4:
        return "E"
    elif num == 5:
        return "F"
    elif num == 6:
        return "G"
    elif num == 7:
        return "H"
    elif num == 8:
        return "I"
    else:
        # Should never reach here
        return "-1"


def main():

    # --------------------------- PLAYERS SETUP ------------------------------
    
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
            # Let player 1 be human for now, but should be completely arbitrary
            # and open to swapping at any point
            AI1_on = False
            AI2_on = True
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



    # --------------------------- AI PARAMETERS ------------------------------

    # Can set an input depth for each AI in this module, or through user input
    input_depth1 = 4   # Arbitrary default value
    input_depth2 = 4   # Arbitrary default value
    if AI1_on:
        while True:
            input_depth1 = str(input("Select the desired difficulty for AI1 (1 - Very Easy, 2 - Easy, 3 - Medium, 4 - Hard): "))
            if input_depth1 not in ["1", "2", "3", "4"]:
                print("Invalid difficulty. Needs to be between 1 and 4.\n")
                continue
            break
    if AI2_on:
        while True:
            input_depth2 = str(input("Select the desired difficulty for AI2 (1 - Very Easy, 2 - Easy, 3 - Medium, 4 - Hard): "))
            if input_depth2 not in ["1", "2", "3", "4"]:
                print("Invalid difficulty. Needs to be between 1 and 4.\n")
                continue
            break


    # ----------------------------- GAME LOOP ---------------------------------

    # Build initial Gamestate
    # Player 1 will be Red (True), Player 2 will be Black (False)
    current_state = Gamestate(redpieces, blackpieces, True, None, None)
    
    while True:

        # End the function when one player (or AI) wins
        if current_state.won == 1:
            print("\n\n")
            print_board_2(update_board_from_grid(current_state.grid))
            print("\n\nThe game has been won by the Red player!")
            return
        elif current_state.won == -1:
            print("\n\n")
            print_board_2(update_board_from_grid(current_state.grid))
            print("\n\nThe game has been won by the Black player!")
            return

        gametree = GameTree(current_state, 1)
        test2 = gametree.move()
        if test2 == "no moves":
            if current_state.turn:
                print("\n\nThe game has been won by the Black player!")
                return
            print("\n\nThe game has been won by the Red player!")
            return

        print_board_2(update_board_from_grid(current_state.grid))
        
        # Take in next move
        if current_state.turn: # Red turn (True)    
            if AI1_on:
                print("Red AI is thinking...")
                gametree = GameTree(current_state, int(input_depth1))
                test = gametree.move()
                if test != "no moves":
                    current_state = test
                    x0 = num_to_letter(current_state.move[0].pos.x)
                    y0 = current_state.move[0].pos.y
                    x1 = num_to_letter(current_state.move[1].pos.x)
                    y1 = current_state.move[1].pos.y
                    printstr = "AI Red Player moved piece {} from {}{} to {}{}".format(current_state.move[0].name, x0, y0, x1, y1)
                    if current_state.eliminated != None:
                        printstr += " and eliminated Black player's piece {}".format(current_state.eliminated.name)
                    printstr += "\n"
                    print(printstr)
                else:
                    print("\n\nThe game has been won by the Black player!")
                    return                   
                continue

            else:   # Human player

                input_str = input("\nRed Player, enter the piece code and destination.\nType \"help\" for help, type \"rules\" for rules, and type \"end\" to end the game: ")

                if input_str == "help":
                    print_help()
                    continue
                elif input_str == "rules":
                    print_rules()
                    continue
                elif input_str == "end":
                    print("Red player has ended the game!")
                    return

                temp = format_input(input_str, current_state.turn)
                if temp == (-1, -1):
                    continue
                piecename = temp[0]
                coord = tuple(temp[1])

                if piecename == -1 or coord == -1:
                    # Invalid entry. Print is handled inside the format_input function
                    # Go for another attempted input
                    print("Caught in -1 return place")
                    continue
                else:
                    test = player_move(piecename, coord, current_state)
                    if test == None:
                        print("Invalid move. This piece is unable to go to the desired location.")
                        continue
                    else:
                        # Do I need to use the whole previous_piece, new_piece stuff and built a new Gamestate object?
                        current_state = test
                        x0 = num_to_letter(current_state.move[0].pos.x)
                        y0 = current_state.move[0].pos.y
                        x1 = num_to_letter(current_state.move[1].pos.x)
                        y1 = current_state.move[1].pos.y
                        printstr = "Red Player moved piece {} from {}{} to {}{}".format(current_state.move[0].name, x0, y0, x1, y1)
                        if current_state.eliminated != None:
                            printstr += " and eliminated Black player's piece {}".format(current_state.eliminated.name)
                        printstr += "\n"                        
                        print(printstr)
                        continue

                    
        else:   # Black turn (False)
            if AI2_on:
                print("Black AI is thinking...")
                gametree = GameTree(current_state, int(input_depth2))
                test = gametree.move()
                if test != "no moves":
                    current_state = test
                    x0 = num_to_letter(current_state.move[0].pos.x)
                    y0 = current_state.move[0].pos.y
                    x1 = num_to_letter(current_state.move[1].pos.x)
                    y1 = current_state.move[1].pos.y
                    printstr = "Black Player moved piece {} from {}{} to {}{}".format(current_state.move[0].name, x0, y0, x1, y1)
                    if current_state.eliminated != None:
                        printstr += " and eliminated Red player's piece {}".format(current_state.eliminated.name)
                    printstr += "\n"
                    print(printstr)
                else:
                    print("\n\nThe game has been won by the Red player!")
                    return                   
                continue
                
            else:   # Human player

                input_str = input("\nBlack Player, enter the piece code and destination.\nType \"help\" for help, type \"rules\" for rules, and type \"end\" to end the game: ")

                if input_str == "help":
                    print_help()
                    continue
                elif input_str == "rules":
                    print_rules()
                    continue
                elif input_str == "end":
                    print("Black player has ended the game!")
                    return
                
                temp = format_input(input_str, current_state.turn)
                piecename = temp[0]
                coord = temp[1]

                if piecename == -1 or coord == -1:
                    # Invalid entry. Print is handled inside the format_input function
                    # Go for another attempted input
                    continue
                else:
                    test = player_move(piecename, coord, current_state)
                    if test == None:
                        print("Invalid move. This piece is unable to go to the desired location.\n")
                        continue
                    else:                        
                        current_state = test
                        x0 = num_to_letter(current_state.move[0].pos.x)
                        y0 = current_state.move[0].pos.y
                        x1 = num_to_letter(current_state.move[1].pos.x)
                        y1 = current_state.move[1].pos.y
                        printstr = "Black Player moved piece {} from {}{} to {}{}".format(current_state.move[0].name, x0, y0, x1, y1)
                        if current_state.eliminated != None:
                            printstr += " and eliminated Red player's piece {}".format(current_state.eliminated.name)
                        printstr += "\n"
                        print(printstr)
    return

main()
