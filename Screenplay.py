import curses
import time
from curses import wrapper

def drawdot(mywin, x, y, dotsize, color):
    i=-(dotsize//2)
    while i <= (dotsize//2):
        j=-(dotsize//2)
        while j <= (dotsize//2):
            mywin.addstr(y+i, x+j,"X", curses.color_pair(color))
            j+=1
        i+=1
    return

def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses.noecho()
    mywin=curses.newwin(50,50,0,0)
    i=2
    curses.start_color()
    mywin.border()
    mywin.refresh()
    mywin.timeout(5000)
    while i<45:
        j=2
        while j<45:
            mywin.clear()
            curses.init_pair(i+j+1,i%10,j%10)
            drawdot(mywin, j, i, 3, i+j+1)
            time.sleep(1)
            mywin.refresh()
            j+=4
        i+=4
    mywin.timeout(5000)
    mywin.getkey()

wrapper(main)
