'''
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
???        - Cannons can be exchanged for horses immediately from their
           starting positions (?????????WAT???????)

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
