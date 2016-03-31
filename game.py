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

       0      1      2      3      4      5      6      7      8
       
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
    for col in range(len(board)):
        s += str(col) + '      '
    print(s)
    print("\n")


def print_help():
    ''' Helper function for printing the help table. No parameters or return.'''
    
    print("\n\n------------------------------------ HELP -------------------------------------- ")
    print("A move is made by a user input of the form:\n\t- 3 character piece code\n\t- Tuple containing position where that piece will move\n\t(these two arguments are on the same line, separated by a space)\n")
    print("The character code is of the following form: [player colour].[piece name letter].[piece number]\n")
    print("The player colour is either 'R' for red, or 'B' for black.\nA player can only move his/her own pieces.\n")
    print("The piece name letter is a letter corresponding to the piece type:\n\tG = general\n\tA = advisor\n\tE = elephant\n\tH = horse\n\tR = chariot\n\tC = cannon\n\tS = soldier\n")
    print("The piece number corresponds to the that piece type the player wishes to move.\nType \"print\" to see the game board.\n\n")
    print("The coordinates for this piece's destination must be inputted as a tuple of (x,y).\nIn this board, x ranges from 0 to 9, and y from 0 to 8 (origin is at the top left)\n\n")
    print("Type \"print\" to view the game board\n")
    print("An example of a valid input would be \"RA1 (4,1)\"\n")
    print("--------------------------------------------------------------------------------\n\n")
    return


def format_input(input_str, turn):
    ''' Takes turn and input string as parameters.
    Formats formats the input string into the proper piece name and
    destination coordinate. Also catches improper inputs and prints the
    reason for the improper input, then returns -1, -1.

    Expect input of the form "RA1 (4,1)" (not case sensitive)
    If successful, this function returns piecename and the coordinate as a list.
    '''

    input_str = input_str.split(" ")
    if len(input_str) != 2:
        print("Incorrect number of input arguments.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1

    if len(input_str[0]) != 3:
        print("Incorrect piece code length.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1

    if len(input_str[1]) != 5:
        print("Incorrect coordinate input length.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1

    if input_str[1][0] != "(" or input_str[1][4] != ")" or input_str[1][2] != ",":
        print("Incorrect formatting for the inputted coordinates.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1

    # The lengths are good, now checking for valid input and building piecename
    tempcolour = input_str[0][0].upper()
    tempname = input_str[0][1].upper()
    tempnumber = str(input_str[0][2])
    tempx = str(input_str[1][1])
    tempy = str(input_str[1][3])
    piecename = ""
    coord = []


    # Colour
    if tempcolour == "R":
        if not turn:
            print("Cannot move opponent's pieces.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += "red."
    elif tempcolour == "B":
        if turn:
            print("Cannot move opponent's pieces.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += "black."
    else:
        print("Invalid piece colour.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1


    # Piece name letter and number
    if tempname == "G":
        piecename += "general."
        if tempnumber != "0":
            print("Invalid piece number. The general can only have number 0.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "A":
        piecename += "advisor."
        if tempnumber not in ["0", "1"]:
            print("Invalid piece number. The advisor can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "E":
        piecename += "elephant."
        if tempnumber not in ["0", "1"]:
            print("Invalid piece number. The elephant can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "H":
        piecename += "horse."
        if tempnumber not in ["0", "1"]:
            print("Invalid piece number. The horse can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "R":
        piecename += "chariot."
        if tempnumber not in ["0", "1"]:
            print("Invalid piece number. The chariot can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "C":
        piecename += "cannon."
        if tempnumber not in ["0", "1"]:
            print("Invalid piece number. The cannon can only have numbers 0 or 1.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    elif tempname == "S":
        piecename += "soldier."
        if tempnumber not in ["0", "1", "2", "3", "4"]:
            print("Invalid piece number. The soldier can only have numbers 0, 1, 2, 3, or 4.")
            print("Try again. Type \"help\" for help if needed.")
            return -1, -1
        piecename += tempnumber
        
    else:
        print("Invalid piece name letter.")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1


    # If we got here, the piecename is valid. Now we handle the coordinates
    if tempx not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
        print("Invalid x coordinate. x coordinates should be between 0 and 8")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1
    if tempy not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print("Invalid y coordinate. y coordinates should be between 0 and 9")
        print("Try again. Type \"help\" for help if needed.")
        return -1, -1
    coord = [int(tempx), int(tempy)]
    
    return [piecename, coord]


def player_move(piecename, coords, current_state):
    ''' Takes as input the piecename and coords determined in format_input for
    the piece being moved, as well as the current state of the game.
    Will check if the move is possible.
    If so it will return the gamestate after this move has been made.
    If not it will return None.
    '''

    if current_state.turn:
        foundFlag = False
        for piece in current_state.t_pieces:
            if piece.name == piecename:
                print(piece.name)
                foundFlag = True
                results = piece.check(tuple(coords), current_state.grid)
                if not results[0]:  # Not a valid move
                    return None
                else:   # Valid move
                    F = current_state.f_pieces[:]
                    if results[1]:  # Eliminate an opponent's piece
                        for elim_piece in current_state.f_pieces:
                            if elim_piece.name == results[1]:
                                F.remove(elim_piece)
                                break
                    newpiece = Piece(Position(coords[0], coords[1]), piece.color, piece.name)
                    T = current_state.t_pieces[:]
                    T.remove(piece)
                    T.append(newpiece)
                    return Gamestate(T, F, not current_state.turn, piece, newpiece)
        print("\nInvalid move. Tried to move a piece that is no longer in play.")
        return None

    else:
        foundFlag = False
        for piece in current_state.f_pieces:
            if piece.name == piecename:
                foundFlag = True
                results = piece.check(tuple(coords), current_state.grid)
                if not results[0]:  # Not a valid move
                    return None
                else:   # Valid move
                    T = current_state.t_pieces[:]
                    if results[1]:  # Eliminate an opponent's piece
                        for elim_piece in current_state.t_pieces:
                            if elim_piece.name == results[1]:
                                T.remove(elim_piece)
                                break
                    newpiece = Piece(Position(coords[0], coords[1]), piece.color, piece.name)
                    F = current_state.f_pieces[:]
                    F.remove(piece)
                    F.append(newpiece)
                    return Gamestate(T, F, not current_state.turn, piece, newpiece)
        print("Invalid move. Tried to move a piece that is no longer in play.")
        return None


def main():
    
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

    # Can set an input depth for each AI in this module, or through user input
    input_depth1 = 5   # Arbitrary default value
    input_depth2 = 5   # Arbitrary default value
    if AI1_on:
        while True:
            input_depth1 = str(input("Select the desired search depth for AI1: "))
            #if len(input_depth1) != 1 or input_depth1 <= "0" or input_depth1 > "9":
            if input_depth1 not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                print("Invalid depth. Needs to be between 0 and 9.\n")
                continue
            break
    if AI2_on:
        while True:
            input_depth2 = str(input("Select the desired search depth for AI2: "))
            #if len(input_depth2) != 1 or input_depth2 <= '0' or input_depth2 > '9':
            if input_depth2 not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                print("Invalid depth. Needs to be between 0 and 9.\n")
                continue
            break



    # WILL SEE LATER WHAT ELSE MAY NEED TO BE INPUTTED AS PARAMETERS FOR EACH AI



    # Build initial Gamestate
    # Player 1 will be Red (True), Player 2 will be Black (False)
    current_state = Gamestate(redpieces, blackpieces, True, None, None)
    #print_board_2(update_board_from_pieces(newgame.t_pieces + newgame.f_pieces))
    #print_board_2(update_board_from_grid(newgame.grid))

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

        print_board_2(update_board_from_grid(current_state.grid))
        
        if current_state.turn: # Red turn (True)    
            if AI1_on:
                gametree = GameTree(current_state, int(input_depth1))
                current_state = gametree.move()
                continue

            else:   # Human player

                input_str = input("\nRed Player, enter the piece code and destination.\nType \"print\" to print the game board, and type \"help\" for help: ")

                if input_str == "help":
                    print_help()
                    continue
                elif input_str == "print":
                    print("-------------------------------- PRINT ------------------------------- ")
                    print_board_2(update_board_from_grid(current_state.grid))
                    print("-------------------------------- PRINT ------------------------------- ")
                    continue

                temp = format_input(input_str, current_state.turn)
                piecename = temp[0]
                coord = tuple(temp[1])
                print("piecename: {}, coord: {}".format(piecename, coord))

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
                        #current_state.turn = not current_state.turn
                        print("finished the round")
                        continue

                    
        else:   # Black turn (False)
            if AI2_on:
                gametree = GameTree(current_state, int(input_depth2))
                current_state = gametree.move()
                continue
                
            else:

                input_str = input("\nBlack Player, enter the piece code and destination.\nType \"print\" to print the game board, and type \"help\" for help: ")

                if input_str == "help":
                    print_help()
                    continue
                elif input_str == "print":
                    print("-------------------------------- PRINT ------------------------------- ")
                    print_board_2(update_board_from_grid(current_state.grid))
                    print("-------------------------------- PRINT ------------------------------- ")
                    continue
                
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
                        # Do I need to use the whole previous_piece, new_piece stuff and built a new Gamestate object?
                        current_state = test
                        #current_state.turn = not current_state.turn
                        #current_state = Gamestate(test.f_pieces, test.t_pieces, not test.turn, test.previous_piece, test.new_piece)
                        
            #current_state.turn = not current_state.turn
            #current_state = Gamestate(current_state.f_pieces, current_state.t_pieces, not current_state.turn, )
    return

main()




'''
K WHERE THINGS STAND NOW (OUTSTANDING ISSUES):

1) Horse blocking does not work (if something is right in fron of the horse, it
   will not be blocked even though it should.
2) Nothing stopping advisors from facing each other
3) Nothing stopping elephant from crossing the river
4) Nothing stopping the general or advisors from leaving the tent
5) Rook can jump over pretty much anything (I believe all pieces can jump)

Nevermind. Pieces can literally go anywhere...

WHERE ARE THE PIECE CONSTRAINTS HANDLED?
'''
