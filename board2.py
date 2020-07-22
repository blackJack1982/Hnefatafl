import curses
import time
import argparse
EMPTY_SQUARE=1
BLOCKED_SQUARE=2
BLACK_PIECE=3
KING_PIECE=4
WHITE_PIECE=5



class board:
    def __init__(self, size):
        self.board=dict()
        self.size=size
        for i in range(size):
            for j in range(size):
                if (i,j) in ((0,0), (size-1,0), (0, size-1), (size-1,size-1)):
                    self.board[(i,j)]="Blocked"
                elif (((i==0 or i==size-1) and j>=(size//2-2) and j<=(size//2+2)) or ((j==0 or j== size-1) and i>=(size//2-2) and i<=(size//2+2))):
                    self.board[(i,j)]="Black"
                elif (((i==1 or i==size-2) and j==(size//2)) or ((j==1 or j==size-2) and i==(size//2))):
                    self.board[(i,j)]="Black"
                elif (i==size//2 and j==size//2):
                    self.board[(i,j)]="King"
                elif ((i+j)>=(size-3) and (i+j)<=(size+1) and (abs(i-j)<=2)):
                    self.board[(i,j)]="White"
                else:
                    self.board[(i,j)]="Empty"

    def drawdot(self, mywin, x, y, dotsize, color):
        i=-(dotsize//2)
        while i <= (dotsize//2):
            j=-(dotsize//2)
            while j <= (dotsize//2):
                mywin.addstr(2+4*y+i, 2+4*x+j,"X", curses.color_pair(color))
                j+=1
            i+=1
    def deldot(self, mywin, x, y, dotsize, color):
        i=-(dotsize//2)
        while i <= (dotsize//2):
            j=-(dotsize//2)
            while j <= (dotsize//2):
                mywin.addstr(2+4*y+i, 2+4*x+j,"X", curses.color_pair(color))
                j+=1
            i+=1
    def drawboard(self,mywin):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[(i,j)]=="Blocked":
                    self.drawdot(mywin, i, j, 3, BLOCKED_SQUARE)
                elif self.board[(i,j)]=="Black":
                    self.drawdot(mywin, i, j, 3, BLACK_PIECE)
                elif self.board[(i,j)]=="White":
                    self.drawdot(mywin, i, j, 3, WHITE_PIECE)
                elif self.board[(i,j)]=="King":
                    self.drawdot(mywin, i, j, 3, KING_PIECE)
                else:
                    self.drawdot(mywin,i,j,3, EMPTY_SQUARE)
        mywin.refresh()

    def check_path(self,piece_x, piece_y, destination_x, destination_y, white_plays):
        acceptable_path=False
        if (white_plays and self.board[piece_x, piece_y]=="White") or (not white_plays and self.board[piece_x, piece_y]=="Black"):
            if (piece_y==destination_y) :
                j=piece_y
                acceptable_path=True
                if(piece_x>destination_x):
                    i_incr=-1
                    i=piece_x+i_incr
                    while i>=destination_x:
                        acceptable_path=(acceptable_path and (self.board[(i,j)]=="Empty")) #test
                        #add check if the destination is not breaking the rule on usage of central cell
                        i+=i_incr
                if(piece_x<destination_x):
                    i_incr=1
                    i=piece_x+i_incr
                    while i<=destination_x:
                        acceptable_path=(acceptable_path and (self.board[(i,j)]=="Empty")) #test
                        #add check if the destination is not breaking the rule on usage of central cell
                        i+=i_incr
                
            elif (piece_x==destination_x): 
                i=piece_x
                acceptable_path=True
                if(piece_y>destination_y):
                    j_incr=-1
                    j=piece_y+j_incr
                    while j>=destination_y:
                        acceptable_path=(acceptable_path and (self.board[(i,j)]=="Empty")) #test
                        #add check if the destination is not breaking the rule on usage of central cell
                        j+=j_incr
                if(piece_y<destination_y):
                    j_incr=1
                    j=piece_y+j_incr
                    while j<=destination_x:
                        acceptable_path=(acceptable_path and (self.board[(i,j)]=="Empty")) #test
                        #add check if the destination is not breaking the rule on usage of central cell
                        j+=j_incr
        return acceptable_path
    
    
    
    def movepiece(self, mywin, piece_x, piece_y, destination_x, destination_y, dot_size, white_plays):
        possible_move=self.check_path(piece_x, piece_y, destination_x, destination_y, white_plays)
        if possible_move:
            old_color=self.board[(piece_x, piece_y)]
            self.board[(piece_x,piece_y)]="Empty"
            self.board[(destination_x, destination_y)]=old_color
            self.drawboard(mywin)
        return possible_move

def main(stdscr):
    
    parser=argparse.ArgumentParser(description="Hnefatafl game")
    parser.add_argument('-b', action="store", dest="board_size", type=int, help="This is the size of the board, please choose 11 or 13")
    parser.add_argument('-w', action="store_true", dest="whites", default=False, help="Says if you want to play whites")
    my_args=parser.parse_args()
    board_size=my_args.board_size
    stdscr.clear()
    curses.noecho()
    curses.curs_set(0)
    curses.mousemask(1)
    mywin=curses.newwin((board_size+1)*4,(board_size+1)*4,0,0)
    mywin2=curses.newwin((board_size+1)*4,30,0,(board_size+1)*4)
    mywin.keypad(1)
    line=1
    mywin2.refresh()
    curses.start_color()
    mywin.border()
    mywin.refresh()
    
    myboard=board(board_size)
    
    curses.init_pair(EMPTY_SQUARE, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    curses.init_pair(BLOCKED_SQUARE, curses.COLOR_RED, curses.COLOR_RED)
    
    curses.init_pair(BLACK_PIECE, curses.COLOR_BLUE, curses.COLOR_BLUE)
    
    curses.init_pair(KING_PIECE, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    
    curses.init_pair(WHITE_PIECE, curses.COLOR_WHITE, curses.COLOR_WHITE)
    
    myboard.drawboard(mywin)

    Game_Finished=False
    mywin2.addstr("Player1: What is your name? ")
    Name_Player1=str(mywin2.getstr()) #check why display is funny
    mywin2.addstr("Player2: What is your name? ")
    Name_Player2=str(mywin2.getstr())
    if my_args.whites:
        mywin2.addstr(Name_Player1+", you play whites") #check why display is funny
    else:
        mywin2.addstr(Name_Player2+", you play whites")
    mywin2.refresh()
    white_is_next=True
    while not Game_Finished:
        if ((my_args.whites and white_is_next) or (not my_args.whites and not white_is_next)):
            mywin2.addstr(Name_Player1+" : your turn")
        else:
            mywin2.addstr(Name_Player2+" : your turn")
        mywin2.refresh()
        line+=1
        mywin.keypad(1)
        while True:
            event=mywin.getch()
            if event == curses.KEY_MOUSE:
                _, piece_x, piece_y, _, _ = curses.getmouse()
                mywin2.addstr("Piece selected, please select destination\n")
                line+=1
                mywin2.refresh()
                while True:
                    event2=mywin.getch()
                    if event2 == curses.KEY_MOUSE:
                        _, destination_x, destination_y, _, _ = curses.getmouse()
                        mywin2.addstr("Destination selected\n")
                        line+=1
                        mywin2.refresh()
                        result=myboard.movepiece(mywin, (piece_x-2)//4, (piece_y-2)//4, (destination_x-2)//4, (destination_y-2)//4, 3,white_is_next)
                        #here comes the code to check if a piece is captured or game is finished
                        if result:
                            mywin2.addstr("Move done\n")
                            line+=1
                            white_is_next=not white_is_next
                        else:
                            mywin2.addstr("Unacceptable move\n")
                            line+=1
                        mywin2.refresh()
                        mywin.refresh()
                        break
                    else:
                        pass
                break
            elif event==ord("q"):
                exit()
            else:
                pass
            mywin.refresh()
            if line>30:
                line=0
                mywin2.clear()
            mywin2.refresh()
curses.wrapper(main)
