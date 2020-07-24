#!/usr/bin/python3
import sys #for exceptions ??
import operator

class BoardError(Exception):
    """Base class for exceptions in this module.
       
    Attributes :
        message -- explanation of the error
    """

    def __init__(self, message : str):
        self.message = message


class Board():

    TYPES : dict = {
            "9x9" : {
                  'restricted_squares' : [ (   0,   0), 
                                           (   0, 9-1), 
                                           (   4,   4), 
                                           ( 9-1,   0), 
                                           ( 9-1, 9-1)],
                  'winning_squares'    : [ (   0,   0), 
                                           (   0, 9-1), 
                                           ( 9-1,   0), 
                                           ( 9-1, 9-1)], 
                  'blues'  : [(0, 3), (0, 4), (0, 5), (1, 4), (3, 0), (3, 8), (4, 0),  (4, 1), 
                              (4, 7), (4, 8), (5, 0), (5, 8), (7, 4), (8, 3), (8, 4),  (8, 5)],
                  'whites' : [(2, 4), (3, 4), (4, 2), (4, 3), (4, 5), (4, 6), (5, 4), (6, 4)],
                  'king' : (4,4)
                },
            "11x11" : {
                  'restricted_squares' : [ (    0,    0), 
                                           (    0, 11-1), 
                                           (    5,    5), 
                                           ( 11-1,    0), 
                                           ( 11-1, 11-1)],
                  'winning_squares'    : [ (    0,    0), 
                                           (    0, 11-1), 
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
                },
            "target1": {
                  'restricted_squares' : [ (    0,    0), 
                                           (    0, 11-1), 
                                           (    5,    5), 
                                           ( 11-1,    0), 
                                           ( 11-1, 11-1)],
                  'winning_squares'    : [ (    0,    0), 
                                           (    0, 11-1), 
                                           ( 11-1,    0), 
                                           ( 11-1, 11-1)],
                  'blues'  : [ (7,1), (5,3), (7,5), (9,3)],   
                  'whites' : [ (7,2), (6,3), (7,4)] 
 
                }
    }
    
    def __init__(self, size : int, type=None, player : str = 'W'):
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
        self.destination = None

        if type is None:
            if self.N == 9:
                self.type = "9x9"
            elif self.N == 11:
                self.type = "11x11"
        else:
            self.type = type

        # create NXN board filled with '-'
        self.board : dict = {(i,j):'-' for i in range(self.N) for j in range(self.N)}      
       
        # Pre-positionning of the player's pieces
        self.restricted_squares = self.TYPES[self.type]['restricted_squares']
        self.winning_squares    = self.TYPES[self.type]['winning_squares']

        for restricted in self.restricted_squares:
            self.board[restricted] = '/'
        
        if "blues" in self.TYPES[self.type]:
            blues = self.TYPES[self.type]['blues']
            
            for blue_piece in blues:
                self.board[blue_piece] = 'B'
        
        if "whites" in self.TYPES[self.type]:
            whites  = self.TYPES[self.type]['whites']
            
            for white_piece in whites:
                self.board[white_piece] = 'W'
            
        if "king" in self.TYPES[self.type]:
            king = self.TYPES[self.type]['king']
            self.destination = king            
            self.board[king] = 'K'

        if self.destination is None:
            self.destination = (4,4) #Oh dear me


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
            self.destination = (3,3)
            return True
        else:
            return False


    def move(self, x: int, y:int) -> bool:
        # (i,j) == current position
        # (x,y) == destination

        #0. Check wether an origin (i,j) has been selected trough select()
        if self.selected != None:
            i, j = self.selected
        else:
            raise BoardError("Please select a piece to be moved")
        
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
        self.destination = None
        

       
        #2) Some rules have to be implemented here
        #
        # Will check to the LEFT, RIGHT, ABOVE and BELLOW the new position
        # to see if if is inhabitted by an ennemy piece
        #   - so if it's out of boundaries we do nothing
        #   -    if it's not an ennemy we do nothing
        # 
        neighbours : list = [ (x, y-1), # LEFT
                              (x, y+1), # RIGHT
                              (x-1, y), # ABOVE
                              (x+1, y)  # BELOW
        ]

        piece = self.board[x,y] #player who is moving, it's the agressor's move
        for pos in neighbours:

            n, m = pos  # n = line
                        # m = column

            """Check that we are not out of boundaries"""
            if n < 0   or   n >= self.N  or  m < 0  or  m >= self.N  :
               continue  #goes to the next neighbour (next cycle of the loop directly)

            """Check this is a player"""
            square = self.board[n,m] 
            player = None

            if square in ('W','B','K'):
                player = square
            else:
                continue #goes to the next neighbour square

            """Define the ennemies"""
            ennemies : list = []

            if player in ('W','K'):    #'W'hites (swedes 'W' peons or 'K' King)
                ennemies.append('B')   # have only one ennemy the 'B'lacks (moskovites)
            
            elif player == 'B':          #'B'lacks (moskovites) don't have a king
                ennemies = [ 'W', 'K' ]  # and have 2 ennemies the 'W'hites peons and the 'K'ing

            #from pprint import pprint 
            
            #pprint( [ f"At pos({n,m} ", player,ennemies])
            
            """Check LEFT and RIGHT for an HORIZONTAL capture
               Also check the boudaries
            """
            left  : bool = m-1 >= 0 and m-1 < self.N and self.board[n, m-1] in ennemies
            right : bool = m+1 >= 0 and m+1 < self.N and self.board[n, m+1] in ennemies
            horizontal : bool = left and right

            """Check ABOVE and BELOW for a VERTICAL capture
               Also check the boundaries
            """
            above : bool = n-1 >= 0 and n-1 < self.N and self.board[n-1, m] in ennemies
            below : bool = n+1 >= 0 and n+1 < self.N and self.board[n+1, m] in ennemies
            vertical : bool = above and below

            #pprint ( { "left" : left, "right" : right, "above" : above, "below" : below } )
            
            output : str = ""
            if player == 'K' and horizontal and vertical :  #King is captured
                output += "the 'K'ing is captured horizontally and vertically"

            elif horizontal : #horizontal neighbour's pieces are capturing this piece
                self.board[n,m] = '-' if (n,m) not in self.restricted_squares else '/'
                output += f"the player '{player}' is captured horizontally"

            elif vertical : #vertical neighbour's pieces are capturing this piece
                self.board[n,m] = '-' if (n,m) not in self.restricted_squares else '/'
                output += f"the player '{player}' is captured vertically"

            """So far so good, send the output ! """
            if len(output) > 0 :
                print (f"At position ({n,m}{output}")



    def check_rules(self) -> str:
        """
        Check the rules of the games 1 by 1
        Will tell us if there is a winner, if a piece was taken ...
        """
        output : str = ""

        #1) King in a king's square win if on the edges
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i,j] == 'K': 
                    if (i,j) in self.winning_squares:
                        output += "The whites won : the King is in a winning square"

        #2)

        return output

    def status(self) -> str:
        """
        Gives the status of the board ==> Display it
        """
        output : str =''

        first : str = '  i/j'
        for i in range(self.N):
            first += f' {i:>2}  '
        output += first+"\n"

        for i in range(self.N):
            output += f' {i:>3} '
            for j in range (self.N):
                if (i,j) == self.selected and (i,j) != self.destination :
                    output += f" /{self.board[i,j]}\\ "
                    #output += f"\033[7m '{self.board[i,j]}' \033[0m"
                elif (i,j) == self.destination:
                    output += f" |{self.board[i,j]}| "
                else:
                    output += f" '{self.board[i,j]}' "
            output += "\n"
        
        return output

    def target(self, move : str) -> bool:
        """
        moves a cursor on the board e.g 'W' becomes |W| when the cursor
        is on it in self.destination
        """
        deltas : dict = {
            "UP"    : ( -1,  0),
            "DOWN"  : (  1,  0),
            "LEFT"  : (  0, -1),
            "RIGHT" : (  0,  1)
        }

        if self.destination is None:
           self.destination = (3, 3)

        next = tuple(map(operator.add, self.destination, deltas[move])) ;
        x,y = next
        
        if x < 0 or x >= self.N or y < 0 or y >= self.N:
            return False #the next step is outside the boudaries
        else:
            self.destination = next
            return True

    
    def t(self, move) -> str:
        if self.target(move):
            pass
        else:
            print (f'You cannot go outside of the board')

        self.stat()



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
    
    print( "\n" * 25 )
    #Smaller board
    print ("N=9")
    N=9
    print ("board = Board(N)")
    board = Board(N)
    print("print (board.status())")
    print (board.status())
    print("board.s(4,3)")
    board.s(4,3)
    print("board.m(1,3)")
    board.m(1,3)
    print("board.s(4,4)")
    board.s(4,4)
    print("board.m(4,3)")
    board.m(4,3)
    print("board.m(2,3)")
    board.m(2,3)
    """
#python3 -i ./engine.steph.py
>>> board = Board(11,'target1')
>>> board.stat()
  i/j  0    1    2    3    4    5    6    7    8    9   10
   0  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'
   1  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   2  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   3  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   4  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   5  '-'  '-'  '-'  'B'  '-'  '/'  '-'  '-'  '-'  '-'  '-'
   6  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   7  '-'  'B'  'W'  '-'  'W'  'B'  '-'  '-'  '-'  '-'  '-'
   8  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   9  '-'  '-'  '-'  'B'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
  10  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'

self.selected : None
>>> board.s(9,3)
  i/j  0    1    2    3    4    5    6    7    8    9   10
   0  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'
   1  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   2  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   3  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   4  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   5  '-'  '-'  '-'  'B'  '-'  '/'  '-'  '-'  '-'  '-'  '-'
   6  '-'  '-'  '-'  'W'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   7  '-'  'B'  'W'  '-'  'W'  'B'  '-'  '-'  '-'  '-'  '-'
   8  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   9  '-'  '-'  '-'  /B\  '-'  '-'  '-'  '-'  '-'  '-'  '-'
  10  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'

self.selected : (9, 3)
>>> board.m(7,3)
At position ((7, 2)the player 'W' is captured horizontally
At position ((7, 4)the player 'W' is captured horizontally
At position ((6, 3)the player 'W' is captured vertically
  i/j  0    1    2    3    4    5    6    7    8    9   10
   0  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'
   1  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   2  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   3  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   4  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   5  '-'  '-'  '-'  'B'  '-'  '/'  '-'  '-'  '-'  '-'  '-'
   6  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   7  '-'  'B'  '-'  /B\  '-'  'B'  '-'  '-'  '-'  '-'  '-'
   8  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
   9  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'
  10  '/'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '-'  '/'

self.selected : (7, 3)
"""
