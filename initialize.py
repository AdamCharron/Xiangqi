from pieces import *

redpieces = [General(Position(4,0),True,"red.general.0"), \
			 Advisor(Position(3,0),True,"red.advisor.0"), Advisor(Position(5,0),True,"red.advisor.1"), \
			 Elephant(Position(2,0),True,"red.elephant.0"), Elephant(Position(6,0),True,"red.elephant.1"), \
			 Horse(Position(1,0),True,"red.horse.0"), Horse(Position(7,0),True,"red.horse.1"), \
			 Chariot(Position(0,0),True,"red.chariot.0"), Chariot(Position(8,0),True,"red.chariot.1"), \
			 Cannon(Position(1,2),True,"red.cannon.0"), Cannon(Position(7,2),True,"red.cannon.1"), \
			 Soldier(Position(0,3),True,"red.soldier.0"), Soldier(Position(2,3),True,"red.soldier.1"), Soldier(Position(4,3),True,"red.soldier.2"), Soldier(Position(6,3),True,"red.soldier.3"), Soldier(Position(8,3),True,"red.soldier.4") \
			 ]

blackpieces = [General(Position(4,9),False,"black.general.0"), \
			 Advisor(Position(3,9),False,"black.advisor.0"), Advisor(Position(5,9),False,"black.advisor.1"), \
			 Elephant(Position(2,9),False,"black.elephant.0"), Elephant(Position(6,9),False,"black.elephant.1"), \
			 Horse(Position(1,9),False,"black.horse.0"), Horse(Position(7,9),False,"black.horse.1"), \
			 Chariot(Position(0,9),False,"black.chariot.0"), Chariot(Position(8,9),False,"black.chariot.1"), \
			 Cannon(Position(1,7),False,"black.cannon.0"), Cannon(Position(7,7),False,"black.cannon.1"), \
			 Soldier(Position(0,6),False,"black.soldier.0"), Soldier(Position(2,6),False,"black.soldier.1"), Soldier(Position(4,6),False,"black.soldier.2"), Soldier(Position(6,6),False,"black.soldier.3"), Soldier(Position(8,6),False,"black.soldier.4") \
			 ]

total_pieces = redpieces+blackpieces

def update_board(total_pieces):
	board = [[0]*10 for _ in range(9)]
	for piece in total_pieces:
		board[piece.pos.x][piece.pos.y] = piece.name
	return board

def print_board(board):
	for j in range(len(board[0])-1,-1,-1):
		s = ''
		for i in range(len(board)):
			s+=str(board[i][j])
			s+=('\t')
		print(s)
