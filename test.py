#!/usr/bin/env python
"""
Author: Derek Hohls
Date: June 2016
Purpose:
    Demonstrate use of GameReportBuilder module
"""
import argparse
import sys
from bgg import bgg_games
from boardgamegeek.exceptions import BoardGameGeekAPIError
from report_builder import GameReportBuilder
from dummy.game import get_games  # dummy game examples


def parse_args():
    """Create the parser & parse args"""
    parser = argparse.ArgumentParser(
        description='Create a PDF for games from boardgamegeek.com (BGG)')
    parser.add_argument('-u', '--user',
                        help='Name of a boardgamegeek user')
    parser.add_argument('-v', '--version',
                        action='store_true',
                        help='Display version information (and exit)')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Run in debug mode')
    parser.add_argument('-p', '--progress',
                        action='store_true',
                        help='Show progress of access to games from BGG')
    parser.add_argument(
        '-s', '--style',
        help='Print according to a style [summary | compact | full | excel]')
    parser.add_argument('-f', '--file',
                        help='Name of PDF file (default: games.pdf/xls)')
    parser.add_argument('-z', '--zone',
                        help='Use US to get USA date/times and paper-sizes')
    parser.add_argument('-c', '--count',
                        help='Number of games to retrieve (default: 10)')
    parser.add_argument('-g', '--games', nargs='+',
                        help='List of game IDs (ignored if user is supplied)')
    return parser.parse_args()


def main(conf):
    if conf.version:
        print "GameReportBuilder Test - Version 1.1"
        sys.exit(1)
    if conf.debug:
        print "Debug is ON!"
        DEBUG = True
    else:
        DEBUG = False
    username = conf.user
    try:
        count = int(conf.count)
    except:
        count = 10
    out_file = conf.file or 'games.pdf'
    if conf.style and conf.style == 'excel':
        out_file = conf.file or 'games.xls'
    zone = conf.zone or 'UK'
    if zone == 'US':
        tzone = 'US'
        psize = 'Letter'
    else:
        tzone = 'UK'
        psize = 'A4'
    ids = []
    if conf.games:
        _ids = conf.games  # list of game ID's [421, 986, 154638]
        try:
            ids = [int(gid) for gid in _ids]
        except:
            print "The game ID's are incorrect in some way -"\
                  " they must all be numbers!"
            sys.exit(1)
    # FONTS available from:
    # http://www.1001freefonts.com/alegreya_sc.font
    # https://fontlibrary.org/en/font/alegreya
    # Install them on your local system first if you want to use them!
    font_family = ['AlegreyaSansSC', 'Alegreya']

    if DEBUG:
        games = get_games()
    else:
        try:
            if len(ids) > 0:
                games = bgg_games(
                    ids=ids, number=count, progress=conf.progress)
            else:
                games = bgg_games(
                    user=username, number=count, progress=conf.progress)
        except BoardGameGeekAPIError:
            print "Sorry - there was a problem accessing BGG"\
                  " (also check your game ID's)"
            sys.exit(1)

    grb = GameReportBuilder(
        user=username, games=games, filename=out_file, familys=font_family,
        time=tzone, margin=36, size=psize, progress=conf.progress,
        header='AlegreyaSansSCR', body='AlegreyaR')

    try:
        if conf.style:
            grb.print_games(style=conf.style)
        else:
            grb.print_games(style='full')
    except Exception as err:
        print "\nSorry!  There was an expected error: %s" % err


if __name__ == "__main__":
    conf = parse_args()
    main(conf)
