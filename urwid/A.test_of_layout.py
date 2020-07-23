#!/usr/bin/python3
import urwid
from engine_steph import Board, BoardError

class VikingView(urwid.WidgetWrap):

    palette = [
        ('titlebar', 'black', 'white'),
        ('refresh button', 'dark green,bold', 'black'),
        ('quit button', 'dark red,bold', 'black'),
        ('getting quote', 'dark blue', 'black'),
        ('board white', 'white', 'dark green' ),
        ('board black', 'black', 'dark green'),
        ('board king', 'white,bold', 'dark green'),
        ('board empty', 'white'    , 'light gray'),
        ('board selected', 'dark red,bold', 'white')
    ]

    def __init__(self, controller):
        self.controller = controller
        urwid.WidgetWrap.__init__(self, self.main_window())

    def update_Board(self):
        status = self.controller.model.status()
        
        output : list = []
        output.append( ('default','\n') )
        output.append( ('default', status()) )
        output.append( ('default', '\n') )

        text = urwid.Text(output)
        return output


    def main_shadow(self, w):
        """Wrap a shadow and background around widget w."""
        bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
        shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')
    
        bg = urwid.Overlay( shadow, bg,
            ('fixed left', 3), ('fixed right', 1),
            ('fixed top', 2), ('fixed bottom', 1))
        w = urwid.Overlay( w, bg,
            ('fixed left', 2), ('fixed right', 3),
            ('fixed top', 1), ('fixed bottom', 2))
        return w

    def main_window(self):
        header_text = urwid.Text(u'aan het Tafel')
        self.header = urwid.AttrMap(header_text, 'titlebar')

        board_text = urwid.Text(self.update_Board())
        board_filler = urwid.Filler(board_text, valign='top', top=1, bottom=1)
        v_padding = urwid.Padding(board_filler, left=1, right=1)
        self.board_box = urwid.LineBox(v_padding)

        

class VikingController:

    def __init__(self, board):
        self.model = board






