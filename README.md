# Hnefatafl
Little game for becode as a team (Goa Dane &amp; Stéphane Devaux)


[![IMAGE Video explaining the rules of the game](http://img.youtube.com/vi/rwO3AN__kAw/0.jpg)](https://www.youtube.com/watch?v=rwO3AN__kAw)

## Links
- [play in the browser](http://www.lutanho.net/play/hnefatafl.html)
- [the rules (Marvin's rules)](http://aagenielsen.dk/fetlar_rules_en.php)

## How to proceed

We decided to take some time to investigate the different parts of the challenge by ourselves and share our advancements in here.

There seems to be 3 main parts to this program :
- **engine** : It contains :
  - a board : an N by N array (i.e. 8X8, 11X11) or a better data structure (steph: I'm using a dict { (i,j) : char}), each place on that board can have different status 'W' for a white player and 'B' for a black player or 'K' for the white's King. According to the chosen board parameters we set up the pieces on the board.
  - limits : movements can only be done on the X or Y axis, one cannot move on an occupied place (where another player is already present), only the king can go on the central place and on the edges, one cannot move outside of the board (stay between 0 and N-1 for x and y).
  - status : a way to display the board interactively, initially simply a print statement. Later on we'll use curses or else to display it, so a template would be nice.
  - **rules** : After a successful move (one that didn't meet a limit) one need to evaluate the board and apply the correct set of rules (e.g. remove a piece that is 'eaten', decide the winner, ...)
- **command line options** : a small way to capture the options with Argparse or Docopt instead of sys.argv
  - option to chose your role Black(Moskovites) or White(Swedes)
  - option to chose your board (board + rules or always the same rules define by marving regardless ?) so 9X9 or 11X11
- **GUI** : Interactive interface done using Curses,Blessings or Urwid

### Research & POC

We'll take at least the day to do our own research into the different topics

#### Steph
I will create 3 files : 
- [engine.steph.py](engine.steph.py) : (6%) It currently contains the Board Class with a fixed 11x11 pattern, ability do initialize the board with the player's pieces, status() displays the board, ... 
- [options.steph.py](options.steph.py) : (0%) I could try something with sys.argv but I want to try Docopt and see Argparse
- and [gui.steph.py](gui.steph.py) : (0.03%) currently looking at [Urwid](urwid.md), (*stash:*~~Basically looked briefly at the links~~
to share my initial trials and errors on these 3 fronts.

#### Goa


