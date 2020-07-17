# Hnefatafl
Little game for becode as a team (Goa Dane &amp; Stéphane Devaux)

## How to proceed

We decided to take some time to investigate the different parts of the challenge by ourselves and share our advancements in here.

There seems to be 3 main parts to this program :
- **engine** : It contains :
  - a board (or more) : an N by N array (i.e. 8X8, 11X11) or a better data structure, each place on that board can have different status 'W' for a white player and 'B' for a black player. According to the board type chosen, we set up the pieces correctly at this time.
  - limits : movements can only be done on the X or Y axis, one cannot move on an occupied place (where another player is already present), only the king can go on the central place and on the edges, one cannot move outside of the board (stay between 0 and N-1 for x and y).
  - status : a way to display the board interactively, initially simply a print statement. Later on we'll use curses or else to display it, so a template would be nice.
  - **rules** : After a successful move (one that didn't meet a limit) one need to evaluate the board and apply the correct set of rules (e.g. remove a piece that is 'eaten', decide the winner, ...)
- **command line options** : a small way to capture the options with Argparse or Docopt instead of sys.argv
  - option to chose your role Black(Moskovites) or White(Swedes)
  - option to chose your board (board + rules or always the same rules define by marving regardless ?) so 9X9 or 11X11
- **GUI** : Interactive interface done using Curses,Blessings or Urwid

STEPH: I will create 3 files : engine.steph.pl, options.steph.py, and gui.steph.py to share my initial trials and errors on these 3 fronts.


