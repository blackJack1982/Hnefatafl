#!/usr/bin/python3
import urwid

# Set up our color scheme
palette = [
    ('titlebar', 'black', 'white'),
    ('refresh button', 'dark green,bold', 'black'),
    ('quit button', 'dark red,bold', 'black'),
    ('getting quote', 'dark blue', 'black')]

#Create the Header ?!?!
header_text = urwid.Text(u'in het Tafel')
header = urwid.AttrMap(header_text, 'titlebar')


