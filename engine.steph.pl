#!/usr/bin/python3

class Board():
    def __init__(self, size : int):
        self.N : int = size
        self.selected = None
        # create NXN board filled with '-'
        self.board : dict = { (i,j):'-' for i in range(11) for j in range(11) }         
        # Pre-positionning of the player's pieces
        if N == 11:
            for j in range (3,8):
                self.board[  0, j] = 'B'
                self.board[N-1, j] = 'B'
                self.board[  5, j] = 'W'
                self.board[  4, j] = 'W' if j in range(4,7) else '-'
                self.board[  6, j] = 'W' if j in range(4,7) else '-'
            for i in range (3,8):
                self.board[ i,   0] = 'B'
                self.board[ i, N-1] = 'B'	
                self.board[ i,   5] = 'W'
            self.board[   1,   5 ] = 'B'
            self.board[   5,   1 ] = 'B'
            self.board[ N-2,   5 ] = 'B'
            self.board[   5, N-2 ] = 'B'
            self.board[   5,   5 ] = 'K'
        elif N == 9:
            print ("Not implemented yet")
            exit()

    def select(self, i : int, j : int) -> bool:
        if self.board[i,j] in 'BWK':
            self.selected = ( i, j )    
            return True
        else:
            return False

    def move(self, i: int, j:int) -> bool:
        pass

    def status(self) -> None:
        """
        Gives the status of the board ==> Display it
        """
        for i in range(N):
            for j in range (N):
                print (f" '{self.board[i,j]}' ", end='')
            print ("")


if __name__ == '__main__':
    N=11 #Size of the board NXN
    board = Board(N)
    board.status()
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
