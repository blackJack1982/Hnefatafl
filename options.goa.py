'''import argparse
parser = argparse.ArgumentParser()
parser.parse_args()'''


#add help discripition

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print args.echo


