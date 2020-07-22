parser=argparse.ArgumentParser(description="Hnefatafl game")
    parser.add_argument('-b', action="store", dest="board_size", type=int, help="This is the size of the board, please choose 11 or 13")
    parser.add_argument('-w', action="store_true", dest="whites", default=False, help="Says if you want to play whites")
    my_args=parser.parse_args()
    board_size=my_args.board_size'''import argparse
parser = argparse.ArgumentParser()
parser.parse_args()'''


#add help discripition

'''#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("echo", help="echo the string you use here")
#args = parser.parse_args()
#print args.echo'''


