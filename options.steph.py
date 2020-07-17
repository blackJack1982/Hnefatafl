#!/usr/bin/python3
"""Viking's Chess

Usage:
    options.steph.py (--board <NxN>) (--player <color>) 
    options.steph.py --auto

"""
from docopt import docopt
import sys

if __name__ == '__main__':
    args = docopt(__doc__) #, version="Viking's Chess 0.1")
    N : int = 11
    player : str = 'W'

#    import pprint ; pprint.pprint(args); sys.exit()
    if args['--auto']:
        pass
    elif args['--board'] == True:
        if args['<NxN>'] in ('9x9','11x11'):
            N = int(args['<NxN>'][0])
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
