#!/usr/bin/python3

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
        # create NXN board filled with '-'
        self.board : dict = {(i,j):'-' for i in range(self.N) for j in range(self.N)}      
        # Pre-positionning of the player's pieces
        if self.N == 11:
            self.restricted_squares = [ (       0,        0), 
                                        (       0, self.N-1), 
                                        (       5,        5), 
                                        (self.N-1,        0), 
                                        (self.N-1, self.N-1)]

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
        elif N == 9:
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
            return True
        else:
            return False

    def move(self, x: int, y:int) -> bool:
        i, j = self.selected
        #1.Check wether a move can be done
        #
        #1.a) Check wether we are trying to move to a restricted square (king's places)
        if (x, y) in self.restricted_squares:
            raise RuntimeError(f'You cannot move to ({x},{y}), it\' a king\'s '
                               f'place/restricted area')
        #1.b) Check wether the destination is horizontally or vertically reacheable
        #     either the lines (x and i) or the columns (y and j) must be similar
        #     to each other to move in the same column or same line
        #
        if x == i: #will now move vertically
            
            pass
        elif j == y: #will now move horizontally
            pass
        else: #not a horizontal or vertical move
            raise RuntimeError('Tried to move diagonally or the same place')
        pass

    def status(self) -> str:
        """
        Gives the status of the board ==> Display it
        """
        output =''
        for i in range(self.N):
            for j in range (self.N):
                output += f" '{self.board[i,j]}' "
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
