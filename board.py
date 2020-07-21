import curses
import time
from curses import wrapper
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
def main(stdscr):
    stdscr.clear()
    curses.noecho()
    curses.curs_set(0)
    curses.mousemask(1)
    mywin=curses.newwin(70,70,0,0)
    mywin2=curses.newwin(70,70,0,70)
    mywin.keypad(1)
    line=1
    mywin2.addstr(line,0,"%d Welcome %d" %(line, curses.KEY_MOUSE))

    mywin2.refresh()
    curses.start_color()
    mywin.border()
    mywin.refresh()
    board_size=11
    myboard=board(board_size)
    EMPTY_SQUARE=1
    curses.init_pair(EMPTY_SQUARE, curses.COLOR_BLACK, curses.COLOR_BLACK)
    BLOCKED_SQUARE=2
    curses.init_pair(BLOCKED_SQUARE, curses.COLOR_RED, curses.COLOR_RED)
    BLACK_PIECE=3
    curses.init_pair(BLACK_PIECE, curses.COLOR_BLUE, curses.COLOR_BLUE)
    KING_PIECE=4
    curses.init_pair(KING_PIECE, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    WHITE_PIECE=5
    curses.init_pair(WHITE_PIECE, curses.COLOR_WHITE, curses.COLOR_WHITE)
    for i in range(board_size):
        for j in range(board_size):
            #print(type(mywin),i,j, str(3), BLOCKED_SQUARE)
            if myboard.board[(i,j)]=="Blocked":
                myboard.drawdot(mywin, i, j, 3, BLOCKED_SQUARE)
            elif myboard.board[(i,j)]=="Black":
                myboard.drawdot(mywin, i, j, 3, BLACK_PIECE)
            elif myboard.board[(i,j)]=="White":
                myboard.drawdot(mywin, i, j, 3, WHITE_PIECE)
            elif myboard.board[(i,j)]=="King":
                myboard.drawdot(mywin, i, j, 3, KING_PIECE)
            else:
                pass
    mywin.refresh()

    while True:

        line+=1
        mywin.keypad(1)
        event=mywin.getch()
        mywin2.addstr(line,0,"%d event %d" %(line, event))
        mywin2.refresh()
        if event == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            myboard.deldot(mywin, (mx-2)//4, (my-2)//4,3, EMPTY_SQUARE)
            line +=1
            mywin2.addstr(line,0,"%d Mouseclick" %(line))
            mywin.refresh()
            mywin2.refresh()
        elif event==ord("q"):
            exit()

wrapper(main)
