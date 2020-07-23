#!/usr/bin/python3
"""Viking's Chess

Usage:
    game.steph.py (--board <NxN>) (--player <color>) 
    game.steph.py --auto
    game.steph.py type          
    game.steph.py type <type>
"""
from docopt import docopt, DocoptExit
import sys
#my code :
from engine_steph import Board, BoardError


def check_options(args, debug=False): 
    """Check options"""

    if debug:
        from pprint import pprint ; 
        pprint(args) 
    
    
    ret : dict = {  'EXIT' : False,
                       'N' : None,
                   'PLAYER': None,
                    'TYPE' : None,
                     'MSG' : "" 
                 }
    
    if args['--auto']:
        ret['N']      = 11
        ret['TYPE']   = "11x11"
        ret['PLAYER'] = "W"
        ret['EXIT']   = False
            
    elif args['type']:
        if not args['<type>'] or args['<type>'] not in Board.TYPES:
            msg : str = f"Available type/scenario :\n"
            for scenario in Board.TYPES:
                msg += f" - {scenario}\n"

            ret['MSG']  = msg
            ret['EXIT'] = True
        else: 
            ret['TYPE'] = args['<type>']
            
            if ret['TYPE'] not in Board.TYPES:
                ret['MSG'] = "not a valid type"
                ret['EXIT'] = True
            else:
                ret['EXIT'] = False
                if ret['TYPE'] == '11x11':
                    ret['N'] = 11
                elif ret['TYPE'] == '9x9':
                    ret['N'] = 9
                else:
                    ret['N'] = 11 # Yep seems to be the default value
        
    elif args['--board'] :
        if not args['<NxN>'] or args['<NxN>'] not in ('9x9','11x11'):
            ret['EXIT'] = True
            ret['MSG']  = "--board only accepts 9x9 or 11x11"
        
        else:
            ret['TYPE'] = args['<NxN>']
            ret['N'] = int( args['<NxN>'].split('x')[0] )
            ret['EXIT'] = True 
            if args['--player'] :
                if args['<color>'] == 'black':
                    ret['PLAYER'] = 'B'
                    ret['EXIT'] = False
                elif args['<color>'] == 'white':
                    ret['PLAYER'] = 'W'
                    ret['EXIT'] = False
                else:
                    ret['EXIT'] = True
                    ret['MSG'] = "--player only accept black or white"                
    else:
        ret['EXIT'] = True
        ret['MSG']  = "Unless --auto is used --board and --player are mandatory"
        
    return ret

if __name__ == '__main__':

    N : int = None
    TYPE : str = None
    PLAYER : str = None

    #0) Check parameters to define N, TYPE and/or PLAYER
    ret = check_options( docopt(__doc__))

    if ret['EXIT']:
        print (f"{ret['MSG']}")
        sys.exit()
    else:
        if ret['TYPE'] is not None and ret['N'] is not None :
            TYPE = ret['TYPE']
            N    = ret['N']
            board = Board(N,TYPE)
        else:
            print (f'ERROR: some parameters are missing')
            sys.exit()
    if ret['PLAYER'] is not None:
        PLAYER = ret['PLAYER']
    
    #1) Create a GUI witht the board
    '''
    print (f'N = {N}, TYPE = {TYPE}, PLAYER = {PLAYER}')        
    board.stat()
    '''
    #Game logic in pure acii-mode to make out what to do
    MODE='select'

    print "press q [ENTER] or Q [ENTER] to leave whenever prompted for an input"

    if PLAYER is not None:
        print ""






