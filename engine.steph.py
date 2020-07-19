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
    def __init__(self, size : int):
        """
        Creates a dictionary of the size NxN (i.e. 11x11, 9x9) 
        with tuple keys (i,j) and values :
        - 'B' : Black or moskovite piece
        - 'W' : White or swede piece
        - 'K' : King of the White/swede
        - '-' : Empty places
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
        if self.N == 11:
    
            self.restricted_squares = [ (       0,        0), 
                                        (       0, self.N-1), 
                                        (       5,        5), 
                                        (self.N-1,        0), 
                                        (self.N-1, self.N-1)]
            blues = [(0, 3) ,  (0, 4),  (0, 5),  (0, 6),  (0, 7),  (1, 5),  
                     (3, 0) , (3, 10),  (4, 0), (4, 10),  (5, 0),  (5, 1),  
                     (5, 9) , (5, 10),  (6, 0), (6, 10),  (7, 0), (7, 10), 
                     (9, 5) , (10, 3), (10, 4), (10, 5), (10, 6), (10, 7)]
            whites = [(3, 5),  (4, 4),  (4, 5),  (4, 6),  (5, 3),  (5, 4), 
                      (5, 6),  (5, 7),  (6, 4),  (6, 5),  (6, 6),  (7, 5)]
            king = 5,5
            
            for blue_piece in blues:
                self.board[blue_piece] = 'B'
            for white_piece in whites:
                self.board[white_piece] = 'W'
            self.board[king] = 'K'


            """    #let's capture it :
            >>> N = 11
            >>> board = Board(N)
            >>> blues = [ (v,w) for v in range(N) for w in range (N) if board.board[v,w] =='B' ]
            >>> whites = [ (v,w) for v in range(N) for w in range (N) if board.board[v,w] =='W' ]
            
            
            #Old way of manually drawing the board
            for j in range (      3, 8):
                self.board[       0, j] = 'B'
                self.board[self.N-1, j] = 'B'
                self.board[       5, j] = 'W'
                self.board[       4, j] = 'W' if j in range(4,7) else '-'
                self.board[       6, j] = 'W' if j in range(4,7) else '-'
            for i in range (3,8):
                self.board[ i,        0] = 'B'
                self.board[ i, self.N-1] = 'B'	
                self.board[ i,        5] = 'W'
            self.board[        1,        5] = 'B'
            self.board[        5,        1] = 'B'
            self.board[ self.N-2,        5] = 'B'
            self.board[        5, self.N-2] = 'B'
            self.board[        5,        5] = 'K'
            """
        elif self.N == 9:
            self.restricted_squares = [ (       0,        0), 
                                        (       0, self.N-1), 
                                        (       4,        4), 
                                        (self.N-1,        0), 
                                        (self.N-1, self.N-1)]

            blues = [(0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (3, 8), (4, 0), (4, 1), 
                     (4, 7), (4, 8), (5, 0), (5, 8), (7, 4), (8, 3), (8, 4), (8, 5)]
            whites = [(2, 4), (3, 4), (4, 2), (4, 3), (4, 5), (4, 6), (5, 4), (6, 4)]
            king = 4,4

            for blue_piece in blues:
                self.board[blue_piece] = 'B'
            for white_piece in whites:
                self.board[white_piece] = 'W'
            self.board[king] = 'K'

            """Old way of filling  the array.
            Now I litterary give the positions collected trough :
            #blues = [ (v,w) for v in range(9) for w in range (9) if board.board[v,w] =='B' ]
            #whites = [ (v,w) for v in range(9) for w in range (9) if board.board[v,w] =='W' ]
            #

            #Initial way of setting the pieces acording to brute force drawing trough loops
            self.restricted_squares = [ (       0,        0), 
                                        (       0, self.N-1), 
                                        (       4,        4), 
                                        (self.N-1,        0), 
                                        (self.N-1, self.N-1)]

            for j in range (3,6):
                self.board[       0, j] = 'B'
                self.board[self.N-1, j] = 'B'
                #self.board[       4, j] = 'W' if j in range(4,6) else '-'
                #self.board[       6, j] = 'W' if j in range(6,8) else '-'
            for i in range(3,6):
                self.board[ i,        0] = 'B'
                self.board[ i, self.N-1] = 'B'
            self.board[       1,        4] = 'B'
            self.board[       4,        1] = 'B'
            self.board[self.N-2,        4] = 'B'
            self.board[       4, self.N-2] = 'B'
            for j in range(2,7):
                self.board[4,j] = 'W' if j != 4 else 'K'
            for i in range(2,7):
                self.board[i,4] = 'W' if i != 4 else 'K'
            """

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
        i, j = self.selected
        print (f'current: ({i},{j}) --> destination: ({x},{y})')
        #1.Check wether a move can be done
        #1)a) Check wether we are trying to move at the same place
        if (x,y) == self.selected:
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
                steps = range( j+1, y+1, 1)
            else:
                steps = range( j-1, y-1, -1)
            
            print ('next horizontal steps : ')
            for pos in steps:
                print (f'({i},{pos}) contains : {self.board[i,pos]}')
                #print (f'self.player : {self.player}')
                #print (f'self.restricted_squares : { self.restricted_squares }')
                if self.board[i,pos] in ("B","W","K"):
                    raise BoardError("You cannot move on or over another player's piece")
                elif (i,pos) in self.restricted_squares:
                    print ("in restricted square")
                    if self.player != 'K':    
                        raise BoardError("You cannot move on or over a King's square")

        elif j == y: 
            """check vertical path is empty
               same column j == y, we'll move for i to x vertically
            """
            #find out direction
            if x > i:
                steps = range( i+1, x+1, 1)
            else:
                steps = range( i-1, x-1, -1)
            
            print ('next vertical steps:')
            for pos in steps:
                print (f'({pos},{j}) contains : {self.board[pos,j]}')
                #print (f'self.player : {self.player}')
                #print (f'self.restricted_squares : { self.restricted_squares }')
                if self.board[pos, j] in ("B", "W", "K"):
                    raise BoardError("You cannot move on or over another player's piece")
                elif (pos,j) in self.restricted_squares:
                    print ("in restricted square")
                    if  self.player != 'K':
                        raise BoardError("You cannot move on or over a King's square")
        else: 
            #not a horizontal or vertical move
            raise BoardError('Tried to move diagonally')
        
        #Teleport to new position
        self.board[x,y] = self.board[i,j]
        self.board[i,j] = "-"

    def m(self, x : int, y : int) -> None:
        """m(x,y)
        to move and see updated location in python shell
        """
        self.move(x,y)
        self.select(x,y)
        self.stat()

    def s(self, x : int, y : int) -> None:
        """s(x,y)
        to select and see updated board in python shell
        """
        self.select(x,y)
        self.stat()

    def stat(self) -> None:
        """stat()
        give  statsus() and board.selected
        """
        print(self.status())
        print(f"self.selected : {self.selected}")

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
                    output += f"/{self.board[i,j]}\\"
            output += "\n"
        
        return output


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

    N=9
    board = Board(N)
    print (board.status())
