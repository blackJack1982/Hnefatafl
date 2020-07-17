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
            print ("Not implemented yet")
            exit()

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

    def move(self, i: int, j:int) -> bool:
        pass

    def status(self) -> str:
        """
        Gives the status of the board ==> Display it
        """
        output =''
        for i in range(self.N):
            for j in range (self.N):
                output += f" '{self.board[i,j]}' "
            output += '\n'
        
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