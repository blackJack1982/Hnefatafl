#!/usr/bin/python3
from pprint import pprint #to display the array

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
#board[0][3:8]    = 5 * ['B']
#	board[3:8][0]    = 5 * ['B']
#	board[N-1][3:8]  = 5 * ['B']
	#board[3:8][N-1]  = 5 * ['B']
	pass	
elif N == 9:
	print ("Not implemented yet")
	exit()


#TESTS:
status(board)
