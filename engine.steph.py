#!/usr/bin/python3
import sys #for exceptions ??

class BoardError(Exception):
    """Base class for exceptions in this module.
       
    Attributes :
        message -- explanation of the error
    """

    def __init__(self, message : str):
        self.message = message


class Board():

    TYPES : dict = {
            9 : {
                  'restricted_squares' : [ (   0,   0), 
                                           (   0, 9-1), 
                                           (   4,   4), 
                                           ( 9-1,   0), 
                                           ( 9-1, 9-1)],
                  'blues'  : [(0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (3, 8), (4, 0),  (4, 1), 
                              (4, 7), (4, 8), (5, 0), (5, 8), (7, 4), (8, 3), (8, 4),  (8, 5)],
                  'whites' : [(2, 4), (3, 4), (4, 2), (4, 3), (4, 5), (4, 6), (5, 4), (6, 4)],
                  'king' : (4,4)
                },
            11:{
                  'restricted_squares' : [ (    0,    0), 
                                           (    0, 11-1), 
                                           (    5,    5), 
                                           ( 11-1,    0), 
                                           ( 11-1, 11-1)],
                  'blues'  : [ ( 0, 3),  (0, 4),  (0, 5),  (0, 6),  
                                (0, 7),  (1, 5),  (3, 0), (3, 10),
                                (4, 0), (4, 10),  (5, 0),  (5, 1),  
                                (5, 9), (5, 10),  (6, 0), (6, 10),
                                (7, 0), (7, 10),  (9, 5), (10, 3),
                               (10, 4), (10, 5), (10, 6), (10, 7)],
                  'whites' : [  (3, 5),  (4, 4),  (4, 5),  (4, 6),
                                (5, 3),  (5, 4),  (5, 6),  (5, 7),
                                (6, 4),  (6, 5),  (6, 6),  (7, 5)],
                  'king' : (5,5)
                }
    }
    
    def __init__(self, size : int):
        """
        Creates a dictionary of the size NxN (i.e. 11x11, 9x9) 
        with tuple keys (i,j) and values :
        - 'B' : Black or moskovite piece
        - 'W' : White or swede piece
        - 'K' : King of the White/swede
        - '-' : Empty places
        - '/' : Empty place but reserved to the King
        N.B. King's reserved locations will be saved as a list of tuples
        First it initializes a NxN dict
        Second, according to N's value pieces are set on the board accordingly
        """
        self.N : int = size
        self.selected = None
        self.player = None
        
        # create NXN board filled with '-'
        self.board : dict = {(i,j):'-' for i in range(self.N) for j in range(self.N)}      
       
        # Pre-positionning of the player's pieces
        self.restricted_squares = self.TYPES[self.N]['restricted_squares']
        blues                   = self.TYPES[self.N]['blues']
        whites                  = self.TYPES[self.N]['whites']
        king                    = self.TYPES[self.N]['king']

        for restricted in self.restricted_squares:
            self.board[restricted] = '/'
        for blue_piece in blues:
            self.board[blue_piece] = 'B'
        for white_piece in whites:
            self.board[white_piece] = 'W'
            
        self.board[king] = 'K'


    def select(self, i : int, j : int) -> bool:
        """
        Allow to select a player's piece 'W', 'B' or 'K'
        and save its location into self.selected 
        
        for further use when moving with move()

        Returns True if the select target (position i,j) is a piece
        Returns False if the select target (position i,j) is empty
        
        N.B. return value will be usefull for the GUI
        """
        if self.board[i,j] in 'BWK':
            self.selected = ( i, j )    
            self.player = self.board[i,j]
            return True
        else:
            return False


    def move(self, x: int, y:int) -> bool:
        # (i,j) == current position
        # (x,y) == destination
        i, j = self.selected
        
        #1.Check wether a move can be done
        #1)a) Check wether we are trying to move at the same place
        if (x,y) == (i,j):
            raise BoardError("Tried to move on the same spot "
                             "(destination = current position)")
        
        #1.b) Check wether we are trying to move out of bonds (outside of the array)
        #     N.B. the selection of the move() coordinates should prevent such an issue
        #          from  happenning, but let's check it anyway
        if x < 0 or x >= self.N or y < 0 or y >= self.N:
            raise BoardError(f'You cannot move to ({x},{y}), it is out of bond.'
                              f'The board is {self.N}x{self.N} .')
        
        #1.c) Check wether the destination is horizontally or vertically reacheable
        #     either the lines (x and i) or the columns (y and j) must be similar
        #     to each other to move in the same column or same line
        #
        if i == x: 
            """check horizontal path is empty 
               same line i == x, we'll move from j to y horizontally
            """
            #find out direction
            if y > j: 
                steps = range( j+1, y+1, 1)  # to the RIGHT ---------->
            else:    
                steps = range( j-1, y-1, -1) # to the  LEFT <----------

            for pos in steps:                
                if self.board[i,pos] in ("B","W","K"): 
                    raise BoardError("You cannot move on or over another player's piece")          
                elif (i,pos) in self.restricted_squares: 
                    if self.player != 'K':    
                        raise BoardError("You cannot move on or over a King's square")

        elif j == y: 
            """check vertical path is empty
               same column j == y, we'll move for i to x vertically
            """
            #find out direction
            if x > i: 
                steps = range( i+1, x+1, 1)  # move DOWN  \|/  \|/  \|/ DOWN
            else:  
                steps = range( i-1, x-1, -1) # move   UP  /|\  /|\  /|\   UP

            for pos in steps:
                if self.board[pos, j] in ("B", "W", "K"):
                    raise BoardError("You cannot move on or over another player's piece")
                elif (pos,j) in self.restricted_squares:
                    if  self.player != 'K':
                        raise BoardError("You cannot move on or over a King's square")
        else: 
            raise BoardError('Tried to move diagonally')
        
        #Teleport to new position
        self.board[x,y] = self.board[i,j]
        self.board[i,j] = "-" if (i,j) not in self.restricted_squares else "/"


    def status(self) -> str:
        """
        Gives the status of the board ==> Display it
        """
        output =''
        for i in range(self.N):
            for j in range (self.N):
                if (i,j) != self.selected:
                    output += f" '{self.board[i,j]}' "
                else:
                    #output += f"\033[7m '{self.board[i,j]}' \033[0m"
                    output += f" /{self.board[i,j]}\\ "
            output += "\n"
        
        return output


    """Python Shell functions to try out the board
    """
    def s(self, x : int, y : int) -> None:
        """s(x,y)
        to select and see updated board in python shell
        """
        self.select(x,y)
        self.stat()


    def m(self, x : int, y : int) -> None:
        """m(x,y)
        to move and see updated location in python shell
        """
        self.move(x,y)
        self.select(x,y)
        self.stat()


    def stat(self) -> None:
        """stat()
        give  statsus() and board.selected
        """
        print(self.status())
        print(f"self.selected : {self.selected}")



if __name__ == '__main__':
    N=11 #Size of the board NXN
    board = Board(N)
    print (board.status())
    """
    '-'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '-'
    '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
    '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
    'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
    'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
    'B'  'B'  '-'  'W'  'W'  'K'  'W'  'W'  '-'  'B'  'B'
    'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
    'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
    '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
    '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
    '-'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '-'
    """
    board.select(0,0) #returns False since '-' is neither a 'B' nor a 'W' nor a 'K'
    board.select(5,1) #returns True for the 'B'lack player a.k.a Moskovites
    board.selected    #returns (5,1)
    board.status()
    board.m(5,0)
    
    #Smaller board
    N=9
    board = Board(N)
    print (board.status())
    """
#python3 -i ./engine.step.py
>>> board = Board(11)
>>> board.s(5,3)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  '-'  /W\  'W'  'K'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 3)
>>> board.m(1,3)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  /W\  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  '-'  '-'  'W'  'K'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (1, 3)
>>> board.s(5,4)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  '-'  '-'  /W\  'K'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 4)
>>> board.m(5,2)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  /W\  '-'  '-'  'K'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 2)
>>> board.s(5,5)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  '-'  '-'  /K\  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 5)
>>> board.s(5,3)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  '-'  '-'  /K\  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 5)
>>> board.m(5,3)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  /K\  '-'  '/'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (5, 3)
>>> board.m(2,3)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  /K\  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  '-'  '-'  '/'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (2, 3)
>>> board.m(2,0)
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 /K\  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  '-'  '-'  '/'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (2, 0)
>>> board.m(0,0)
 /K\  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'
 '-'  '-'  '-'  'W'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  'B'  'W'  '-'  '-'  '/'  'W'  'W'  '-'  'B'  'B'
 'B'  '-'  '-'  '-'  'W'  'W'  'W'  '-'  '-'  '-'  'B'
 'B'  '-'  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  'B'
 '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
 '-'  '-'  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'
 '/'  '-'  '-'  'B'  'B'  'B'  'B'  'B'  '-'  '-'  '/'

self.selected : (0, 0)
>>>
"""
