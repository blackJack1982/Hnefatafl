#!/usr/bin/python3
import urwid
from engine_steph import Board, BoardError
#the above doesn't work so :
"""
import imp
with open('engine.steph.py') as fp:
    engine = imp.load_module(
        'Board', fp, 'engine.steph.py',
        ('.py', 'rb', imp.PY_SOURCE)
    )
"""
##SRC
#Unashamedly copied and modified from : https://guru.net.nz/blog/python/ncurses/video/2015/01/21/use-curses-dont-swear.html

# Set up our color scheme
palette = [
    ('titlebar', 'black', 'white'),
    ('refresh button', 'dark green,bold', 'black'),
    ('quit button', 'dark red,bold', 'black'),
    ('getting quote', 'dark blue', 'black'),
    ('board white', 'white', 'dark green' ),
    ('board black', 'black', 'dark green'),
    ('board king', 'white,bold', 'dark green'),
    ('board empty', 'white'    , 'light gray'),
    ('board selected', 'dark red,bold', 'white')]

#Create the Header ?!?!
header_text = urwid.Text(u'aan het Tafel')
header = urwid.AttrMap(header_text, 'titlebar')

#Create the menu (at the bottom of the screen)
menu = urwid.Text([
        u'Press (', ('refresh button', u'R'), u') to refresh ...',
        u'Press (', ('quit button', u'Q'), u') to quit.'])

quote_text = urwid.Text(u'Press (R) to get your first status')
quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(quote_filler, left=1, right=1)
quote_box = urwid.LineBox(v_padding)

# Assemble the widgets into the widget Layout
layout = urwid.Frame(header=header, body=quote_box, footer=menu)

def get_new_status():
    output : list = []
    for i in range(board.N):
        for j in range (board.N):
            #if (i,j) == self.selected:
            if (i,j) == board.selected:
                output.append( ('board selected', board.PLAYER))
            elif board.board[i,j] == 'W' and (i,j) != board.selected:
                output.append( ('board white', board.board[i,j]) )
            elif board.board[i,j] == 'B' and (i,j) != board.selected:
                output.append( ('board black', board.board[i,j]) )
            elif board.board[i,j] == 'K' and (i,j) != board.selected:
                output.append( ('board king', board.board[i,j]) )
            elif board.board[i,j] == '-': 
                output.append( ('board empty', board.board[i,j]) )
            
        output.append( ('default', '\n') )

    #status = board.status()
    output.append( ('default','\n') )
    output.append( ('default', board.status()) )
    output.append( ('default', '\n') )
    #output.append( ('default', u'board.selected : ') )
    output.append( ('default', f"You are player : '{PLAYER}' ") )

    if board.selected is not None:
        output.append( ('default', f"at pos : ({board.selected[0]},{board.selected[1]})") )
    output.append( ('default', "\n") )

    if MODE == "target" :
        output.append( ('default', "you can use the letters g<-, j\/, k/\, l-> to select a target destination") )
        output.append( ('default', "\nyou can press m when you want to move to the | | target"))

    if MODE == "select" :
        output.append( ('default', "you can use the letters g<-, j\/, k/\, l-> to select piece") )
        output.append( ('default', "\nyou can press s when you want to select your piece"))




    text = urwid.Text(output)
    return output

def handle_input(key):
    if key == 'R' or key == 'r':
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())

    elif key == 'h':
        board.target("LEFT")
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
 
    elif key == 'l':
        board.target("RIGHT")
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
 
    elif key == 'j':
        board.target("DOWN")
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
 
    elif key == 'k':
        board.target("UP")
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
    
    elif key == 'm':
        x,y = board.destination

        try:
            board.move(x,y)
            MODE = "select"
            status = get_new_status()
        except BoardError as e:
            status = get_new_status()
            status.append( ('default', f"\n\nERROR : {e}") )

        
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(status)
    
    elif  board.selected is None and key == 's':
        i,j = board.destination

        if board.select(i,j):
            MODE = "target"
            status = get_new_status()
        else:
            status = get_new_status()
            status.append( ('default', "\n\nError: choose one of your pieces ('W','K','B')") )
 
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(status)
 
    elif key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()

N      : int = 11
PLAYER : str = "B"
TYPE   : str = "target1"

board = Board(N, TYPE)
board.select(8,3)
board.PLAYER = PLAYER

MODE = 'select' 
# target = we look for a destination
# select = we chose a piece




main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)

main_loop.run()


