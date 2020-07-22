#!/usr/bin/python3
"""Viking's Chess

Usage:
    game.steph.py (--board <NxN>) (--player <color>) 
    game.steph.py --auto

"""
from docopt import docopt
import sys

def check_options(args):
    """Check options"""
    N : int = 11
    player : str = 'W'

    #import pprint ; pprint.pprint(args); sys.exit()
    if args['--auto']:
        pass
    elif args['--board'] == True:
        if args['<NxN>'] in ('9x9','11x11'):
            N = int( args['<NxN>'].split('x')[0] )
            if args['--player'] == True:
                if args['<color>'] == 'black':
                    player = 'B'
                elif args['<color>'] == 'white':
                    player = 'W'
                else:
                    print ("--player only accept black or white")
                    sys.exit()
        else:
            print ("--board only accepts 9x9 or 11x11")
            sys.exit()
    else:
        print ("Unless --auto is used --board and --player are mandatory")
        sys.exit()
        
    print (f'player:{player} | board:{N}x{N}')

if __name__ == '__main__':
    check_options( docopt(__doc__)) # version="Viking's Chess 0.1")


