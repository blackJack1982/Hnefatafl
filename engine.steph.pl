#!/usr/bin/python3

#1. Create an empty board

N = 11 # could be 9 for 9X9 or 11 for 11X11
board = { (i,j):'-' for i in range(11) for j in range(11) } # create NXN board filled with '-'

#USEFUL: 
def status(board):
    """
	Gives the status of the board ==> Display it
	"""
    for i in range(N):
        for j in range (N):
            print (f" '{board[i,j]}' ", end='')
        print ("")

#2. Positioning of the pieces

if N == 11:
    for j in range (3,8):
        board[  0, j] = 'B'
        board[N-1, j] = 'B'
        board[  5, j] = 'W'
        board[  4, j] = 'W' if j in range(4,7) else '-'
        board[  6, j] = 'W' if j in range(4,7) else '-'
    for i in range (3,8):
        board[ i,   0] = 'B'
        board[ i, N-1] = 'B'	
        board[ i,   5] = 'W'
    board[   1,   5 ] = 'B'
    board[   5,   1 ] = 'B'
    board[ N-2,   5 ] = 'B'
    board[   5, N-2 ] = 'B'
    #       board[ i,   4] = 'W' if j in range(4,7) else '-'
elif N == 9:
    print ("Not implemented yet")
    exit()


#TESTS:
status(board)
