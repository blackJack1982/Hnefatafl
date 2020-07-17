#!/usr/bin/python3
from pprint import pprint #to display the array

N = 11 # could be 9 for 9X9 or 11 for 11X11

board = [ ['-'] * N ] * N # create NXN board filled with '-'

def status(board):
	"""
	Gives the status of the board ==> Display it
	"""
	pprint(board)

status(board)
