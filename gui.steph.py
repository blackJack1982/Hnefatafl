#!/usr/bin/python3
import urwid
#from "engine.steph" import Board
#the above doesn't work so :
import imp
with open('engine.steph.pl') as fp:
    engine = imp.load_module(
        'Board', fp, 'engine.steph.pl',
        ('.pl', 'rb', imp.PY_SOURCE)
    )
#SRC
#Unashamedly copied and modified from : https://guru.net.nz/blog/python/ncurses/video/2015/01/21/use-curses-dont-swear.html

# Set up our color scheme
palette = [
    ('titlebar', 'black', 'white'),
    ('refresh button', 'dark green,bold', 'black'),
    ('quit button', 'dark red,bold', 'black'),
    ('getting quote', 'dark blue', 'black')]

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

def get_new_status() -> str:
    return board.status()

def handle_input(key):
    if key == 'R' or key == 'r':
        quote_box.base_widget.set_text(('getting status', 'Gettingn new status ...'))
        main_loop.draw_screen()
        quote_box.base_widget.set_text(get_new_status())
    
    elif key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()

N : int = 11
board = engine.Board(N)

main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)

main_loop.run()


