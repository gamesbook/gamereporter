# About

**gamereporter** allows you to generate a PDF report for a list of game-like
objects - typically boardgames whose data is sourced from 
[boardgamegeek](http://www.boardgamegeek.com).

# Usage

The `test.py` program can be used to generate a PDF report of game details, or
a game summary (by default, into a file called `games.pdf`).

To see the program options, run:

    python test.py --help
    
A test, or "debug", run with progress display, but requiring no access to 
boardgamegeek.com, with output going to a a file called `dummy.pdf`:

    python test.py -d -p -f dummy.pdf

A 'real' example, to create a detailed game report of 5 games for a boardgamegeek 
user called `shurelock`, who is USA-based, while showing progress, uses:

    python test.py -u shurelock -z US -c 5 -p

A summary report for the same user, but with metric options & no progress:

    python test.py -u shurelock -c 5 -s

**NOTE** `shurelock` is not a real user and so the program will fail!
    
If you know the games you want a report on, pass in their numbers as a list:

    python test.py -p -g 421 154638 986 320

# Features

- Access games by ID from boardgamegeek, or games linked to a user of that site
- Create a PDF with details of each game accessed
- Provide a summary table of games
- Provide some basic parameters (such as fonts and page sizes to be used)

The existing code can, of course, be modified to create other layouts and report
on other game details.

# Requirements

This application assumes you are familiar with Python and its usage via the
command-line.  It has only been used and tested under Ubuntu 14.04, running
Python 2.7.  It is also assumed you are familiar with use of git.

# Installation

Create and activate a [virtualenv](https://virtualenv.pypa.io/en/stable/). 
Clone this application into a directory, change to that directory and run:

    pip install requirements.txt

If you want to use the `test.py` program, you first need to install the Alegreya
TrueType fonts; see:

- ['AlegreyaSansSC'](http://www.1001freefonts.com/alegreya_sans_sc.font)
- ['Alegreya'](https://fontlibrary.org/en/font/alegreya)

# Credits

Lots of thanks go to the authors and developers of the following Python 
libraries for making it even possible to create such a reporting tool:
- [`boardgamegeek`](https://github.com/lcosmin/boardgamegeek)
- [`reportlab`](http://www.reportlab.com/opensource/)

Also, thanks to the creator of the amazingly attractive Alegreya fonts - 
 Juan Pablo del Peral!

