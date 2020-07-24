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

MODE   : str = "select"

def get_new_status(msg : str = ''):
    output : list = []
    output.append( ('default', '\n') )
    output.append( ('default', board.status()) )
    output.append( ('default', '\n') )
    output.append( ('default', msg) )

    if MODE == 'select':
        output.append ( ('default', 'Use the arrow keys to move around\n') )
        output.append ( ('default', 'Use the space bar to SELECT your piece') )
    elif MODE == 'target':
        output.append ( ('default', 'Use the arrow keys to move around\n') )
        output.append ( ('default', 'Use the space bar to TARGET your destination') )

    return output

def handle_input(key):
    global MODE 
    '''
    if key == 'U' or key == 'u':
        #quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
    '''
    msg : str = ''

    if MODE in ( 'select', 'target' ):
        if key == 'up':
            board.target('UP')
        elif key == 'down':
            board.target('DOWN')
        elif key == 'left':
            board.target('LEFT')
        elif key == 'right':
            board.target('RIGHT')
        
        quote_box.base_widget.set_text(get_new_status(msg))

    if MODE == 'select' and  key == ' ':
        i,j = board.destination
            
        if board.select(i,j):
            MODE = 'target'
        else:
            msg =  "Error: choose one of your pieces ( 'W', 'K', 'B' )\n"
            
        quote_box.base_widget.set_text(get_new_status(msg))

    elif MODE == 'target' and  key == ' ':
        x,y = board.destination
            
        try:
            board.move(x,y)
            MODE = 'select'
        except BoardError as e:
            print(e)
            
        quote_box.base_widget.set_text(get_new_status(msg))


    main_loop.draw_screen()
    
    if key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()


N      : int = 11
PLAYER : str = "B"
TYPE   : str = "target1"

board = Board(N, TYPE)
board.select(8,3)
board.PLAYER = PLAYER


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
        u'Press (', ('refresh button', u'U'), u') to update ...',
        u'Press (', ('quit button', u'Q'), u') to quit.'])

quote_text = urwid.Text(get_new_status())
quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(quote_filler, left=1, right=1)
quote_box = urwid.LineBox(v_padding)

# Assemble the widgets into the widget Layout
layout = urwid.Frame(header=header, body=quote_box, footer=menu)

main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)

main_loop.run()
