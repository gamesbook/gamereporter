#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Derek Hohls
Date: June 2016
Purpose:
    BoardGameGeek.com interface for GameReportBuilder
Notes:
    Huge thanks to the developer of the `boardgamegeek` Python Library
"""
# future
from __future__ import division
# lib
import json
import math
import os
import tempfile
# third party
from boardgamegeek import BoardGameGeek
from boardgamegeek.exceptions import BoardGameGeekAPIRetryError


class BGGGameList(object):
    """Lists which are groups of multiple games' string-based properties."""

    def __init__(self):
        """create empty lists to hold values"""
        self.alternative_names = []
        self.artists = []
        self.average = []
        self.averageweight = []
        self.bayesaverage = []
        self.categories = []
        self.description = []
        self.designers = []
        self.expands = []
        self.expansion = []
        self.expansions = []
        self.families = []
        self.id = []
        self.image = []
        self.implementations = []
        self.maxplayers = []
        self.mechanics = []
        self.median = []
        self.minage = []
        self.minplayers = []
        self.name = []
        self.numcomments = []
        self.numweights = []
        self.owned = []
        self.playingtime = []
        self.publishers = []
        self.ranks = []
        self.stddev = []
        self.thumbnail = []
        self.trading = []
        self.usersrated = []
        self.wanting = []
        self.wishing = []
        self.yearpublished = []
        # custom fields
        self.players = []
        self.description_short = []
        self.age = []

    def set_values(self, game):
        """Append a game's property to a matching list."""
        self._game = game  # BGGGame object
        if self._game:
            self.alternative_names.append(self._game.alternative_names)
            self.artists.append(self._game.artists)
            self.average.append(self._game.average)
            self.averageweight.append(self._game.averageweight)
            self.bayesaverage.append(self._game.bayesaverage)
            self.categories.append(self._game.categories)
            self.description_short.append(self._game.description_short)
            self.description.append(self._game.description)
            self.designers.append(self._game.designers)
            self.expands.append(self._game.expands)
            self.expansion.append(self._game.expansion)
            self.expansions.append(self._game.expansions)
            self.families.append(self._game.families)
            self.id.append(self._game.id)
            self.image.append(self._game.image)
            self.implementations.append(self._game.implementations)
            self.maxplayers.append(self._game.maxplayers)
            self.mechanics.append(self._game.mechanics)
            self.median.append(self._game.median)
            self.minage.append(self._game.minage)
            self.minplayers.append(self._game.minplayers)
            self.name.append(self._game.name)
            self.numcomments.append(self._game.numcomments)
            self.numweights.append(self._game.numweights)
            self.owned.append(self._game.owned)
            self.playingtime.append(self._game.playingtime)
            self.publishers.append(self._game.publishers)
            self.ranks.append(self._game.ranks)
            self.stddev.append(self._game.stddev)
            self.thumbnail.append(self._game.thumbnail)
            self.trading.append(self._game.trading)
            self.usersrated.append(self._game.usersrated)
            self.wanting.append(self._game.wanting)
            self.wishing.append(self._game.wishing)
            self.yearpublished.append(self._game.yearpublished)
            # custom fields
            self.players.append(self._game.players)
            self.description_short.append(self._game.description_short)
            self.age.append(self._game.age)


class BGGGame(object):
    """Wrapper around the `game` object from the boardgamegeek API"""

    def __init__(self, game_id, short=500):
        """
        Args:
            short: int
                number of characters to use for short description
        """
        self._game = None
        self.short = int(short) or 500
        self.bgg = BoardGameGeek(disable_ssl=True)
        if isinstance(game_id, int):
            self._game = self.bgg.game(game_id=game_id)
        elif isinstance(game_id, ""):
            self._game = self.bgg.game(name=game_id)
        else:
            print
        self.set_properties()

    def get_description_custom(self):
        """Create a custom, abbreviated description for a game."""
        if self._game:
            desc = self._game.description[0:self.short]
            _cut = int(
                (len(desc) -
                 len(desc.replace(',', '').replace('.', '').replace(':', '')))
                / 2 + self.short)
            desc = self._game.description[0:_cut]
            return desc[0:-3] + '...'

    def HTML_description(self, text):
        """Changes the BGG [] notation to <> and adds line breaks"""
        #print "bgg.self._game.description\n", self._game.description
        return self._game.description.replace('[', '<').replace(']', '>').\
            replace('\n', '<br/>')

    def set_properties(self):
        """Create both raw (_ prefix) and string formatted versions of props"""
        if self._game:
            self._alternative_names = self._game.alternative_names
            self.alternative_names = ', '.join(self._game.alternative_names)
            self._artists = self._game.artists
            self.artists = ', '.join(self._game.artists)
            self._average = self._game.average
            self.average = '%.3f' % self._game.average
            self._averageweight = self._game.averageweight
            self.averageweight = '%.2f' % self._game.averageweight
            self.percentageweight = '%s' % math.ceil(self._game.averageweight * 20.0)
            self._bayesaverage = self._game.bayesaverage
            self.bayesaverage = '%.3f' % self._game.bayesaverage
            self._categories = self._game.categories
            self.categories = ', '.join(self._game.categories)
            self._description = self._game.description
            self.description = '%s' % self._game.description
            self.description_html = '%s' % \
                self.HTML_description(self._game.description)
            try:
                self.description_short = '%s' % self._game.description_short
                self.description_short_html = '%s' % \
                    self.HTML_description(self._game.description_short)
            except AttributeError:
                self.description_short = ''
                self.description_short_html = ''
            self._designers = self._game.designers
            self.designers = ', '.join(self._game.designers)
            self._expands = self._game.expands
            self.expands = ', '.join([exp.name for exp in self._game.expands])
            self._expansion = self._game.expansion
            if self._game.expansion is True:
                self.expansion = 'Yes'
            else:
                self.expansion = 'No'
            self._expansions = self._game.expansions
            self.expansions = ', '.join(
                [exp.name for exp in self._game.expansions])
            self._families = self._game.families
            self.families = ', '.join(self._game.families)
            self._id = self._game.id
            self.id = '%s' % self._game.id
            self._image = self._game.image
            self.image = '%s' % self._game.image
            self._implementations = self._game.implementations
            self.implementations = ', '.join(self._game.implementations)
            self._maxplayers = self._game.maxplayers
            self.maxplayers = '%s' % self._game.maxplayers
            self._mechanics = self._game.mechanics
            self.mechanics = ', '.join(self._game.mechanics)
            self._median = self._game.median
            self.median = '%.3f' % self._game.median
            self._minage = self._game.minage
            self.minage = '%s' % self._game.minage
            self._minplayers = self._game.minplayers
            self.minplayers = '%s' % self._game.minplayers
            self._name = self._game.name
            self.name = '%s' % self._game.name
            self._numcomments = self._game.numcomments
            self.numcomments = '%s' % self._game.numcomments
            self._numweights = self._game.numweights
            self.numweights = '%s' % self._game.numweights
            self._owned = self._game.owned
            self.owned = '%s' % self._game.owned
            self._playingtime = self._game.playingtime
            self.playingtime = '%s' % self._game.playingtime
            self._publishers = self._game.publishers
            self.publishers = ', '.join(self._game.publishers)
            self._ranks = self._game.ranks
            self.ranks = '%s' % self._game.ranks
            self._stddev = self._game.stddev
            self.stddev = '%.3f' % self._game.stddev
            self._thumbnail = self._game.thumbnail
            self.thumbnail = '%s' % self._game.thumbnail
            self._trading = self._game.trading
            self.trading = '%s' % self._game.trading
            self._usersrated = self._game.usersrated
            self.usersrated = '%s' % self._game.usersrated
            self._wanting = self._game.wanting
            self.wanting = '%s' % self._game.wanting
            self._wishing = self._game.wishing
            self.wishing = '%s' % self._game.wishing
            self._yearpublished = self._game.yearpublished
            self.yearpublished = '%s' % self._game.yearpublished
            # custom fields
            self.description_custom = self.get_description_custom()
            self._description_custom = self.description_custom
            if self._game.minplayers == self._game.maxplayers:
                    self.players = '%s' % self._game.maxplayers
            else:
                self.players = '%s-%s' % (self._game.minplayers,
                                          self._game.maxplayers)
            self._players = (self._game.minplayers, self._game.maxplayers)
            self.age = '%s+' % self._game.minage
            self._age = self._game.minage


class GameObject(object):

    def __init__(self, game_dict, short=500):
        """
        Args:
            short: int
                number of characters to use for short description
        """
        self.game_dict = game_dict
        self.short = int(short) or 500
        self.set_properties(self.game_dict)

    def get_description_custom(self):
        """Create a custom, abbreviated description for a game."""
        if self.game_dict:
            desc = self.game_dict.get('_description', '')[0:self.short]
            _cut = int(
                (len(desc) -
                 len(desc.replace(',', '').replace('.', '').replace(':', '')))
                / 2 + self.short)
            desc = self.game_dict.get('_description', '')[0:_cut]
            return desc[0:-3] + '...'

    def HTML_description(self, text):
        """Changes the BGG [] notation to <> and adds line breaks"""
        #print "bgg.self._game.description\n", self._game.description
        return self.game_dict.get('_description', '').replace('[', '<').\
            replace(']', '>').replace('\n', '<br/>')

    def set_properties(self, game_dict):
        """Create both raw (_ prefix) and string formatted versions of props"""
        if game_dict:
            self._alternative_names = game_dict.get('_alternative_names')
            self.alternative_names = ', '.join(game_dict.get('alternative_names'))
            self._artists = game_dict.get('_artists')
            self.artists = ', '.join(game_dict.get('artists'))
            self._average = game_dict.get('_average')
            self.average = '%.3f' % game_dict.get('_average')
            self._averageweight = game_dict.get('_averageweight')
            self.averageweight = '%.2f' % game_dict.get('_averageweight')
            self.percentageweight = \
                '%s' % math.ceil(game_dict.get('_averageweight') * 20.0)
            self._bayesaverage = game_dict.get('_bayesaverage')
            self.bayesaverage = '%.3f' % game_dict.get('_bayesaverage')
            self._categories = game_dict.get('_categories')
            self.categories = ', '.join(game_dict.get('_categories'))
            self._description = game_dict.get('_description')
            self.description = '%s' % game_dict.get('_description')
            self.description_html = '%s' % \
                self.HTML_description(game_dict.get('_description'))
            self.description_short = '%s' % game_dict.get('_description_short')
            self.description_short_html = '%s' % \
                self.HTML_description(game_dict.get('_description_short'))
            self._designers = game_dict.get('_designers')
            self.designers = ', '.join(game_dict.get('_designers'))
            self._expands = game_dict.get('_expands')
            self.expands = \
                ', '.join([exp.name for exp in game_dict.get('_expands')])
            self._expansion = game_dict.get('_expansion')
            if game_dict.get('_expansion') is True:
                self.expansion = 'Yes'
            else:
                self.expansion = 'No'
            self._expansions = game_dict.get('_expansions')
            self.expansions = ', '.join(
                [exp.name for exp in game_dict.get('_expansions')])
            self._families = game_dict.get('_families')
            self.families = ', '.join(game_dict.get('_families'))
            self._id = game_dict.get('_id')
            self.id = '%s' % game_dict.get('_id')
            self._image = game_dict.get('_image')
            self.image = '%s' % game_dict.get('_image')
            self._implementations = game_dict.get('_implementations')
            self.implementations = ', '.join(game_dict.get('_implementations'))
            self._maxplayers = game_dict.get('_maxplayers')
            self.maxplayers = '%s' % game_dict.get('_maxplayers')
            self._mechanics = game_dict.get('_mechanics')
            self.mechanics = ', '.join(game_dict.get('_mechanics'))
            self._median = game_dict.get('_median')
            self.median = '%.3f' % game_dict.get('_median')
            self._minage = game_dict.get('_minage')
            self.minage = '%s' % game_dict.get('_minage')
            self._minplayers = game_dict.get('_minplayers')
            self.minplayers = '%s' % game_dict.get('_minplayers')
            self._name = game_dict.get('_name')
            self.name = '%s' % game_dict.get('_name')
            self._numcomments = game_dict.get('_numcomments')
            self.numcomments = '%s' % game_dict.get('_numcomments')
            self._numweights = game_dict.get('_numweights')
            self.numweights = '%s' % game_dict.get('_numweights')
            self._owned = game_dict.get('_owned')
            self.owned = '%s' % game_dict.get('_owned')
            self._playingtime = game_dict.get('_playingtime')
            self.playingtime = '%s' % game_dict.get('_playingtime')
            self._publishers = game_dict.get('_publishers')
            self.publishers = ', '.join(game_dict.get('_publishers'))
            self._ranks = game_dict.get('_ranks')
            self.ranks = '%s' % game_dict.get('_ranks')
            self._stddev = game_dict.get('_stddev')
            self.stddev = '%.3f' % game_dict.get('_stddev')
            self._thumbnail = game_dict.get('_thumbnail')
            self.thumbnail = '%s' % game_dict.get('_thumbnail')
            self._trading = game_dict.get('_trading')
            self.trading = '%s' % game_dict.get('_trading')
            self._usersrated = game_dict.get('_usersrated')
            self.usersrated = '%s' % game_dict.get('_usersrated')
            self._wanting = game_dict.get('_wanting')
            self.wanting = '%s' % game_dict.get('_wanting')
            self._wishing = game_dict.get('_wishing')
            self.wishing = '%s' % game_dict.get('_wishing')
            self._yearpublished = game_dict.get('_yearpublished')
            self.yearpublished = '%s' % game_dict.get('_yearpublished')
            # custom fields
            self.description_custom = self.get_description_custom()
            self._description_custom = self.description_custom
            if game_dict.get('_minplayers') == game_dict.get('_maxplayers'):
                    self.players = '%s' % game_dict.get('_maxplayers')
            else:
                self.players = '%s-%s' % (game_dict.get('_minplayers'),
                                          game_dict.get('_maxplayers'))
            self._players = (game_dict.get('_minplayers'),
                             game_dict.get('_maxplayers'))
            self.age = '%s+' % game_dict.get('_minage')
            self._age = game_dict.get('_minage')


def bgg_games(ids=None, user=None, filename=None, number=None, progress=False,
              **kwargs):
    """Return a list of BoardGameGeek games; sourced by ID, or user, or file

    Args:
        ids: list
            games IDs (integers) used by BGG
        user: string
            BGG user name; if supplied, then :
            * IDs will be ignored
        filename: string
            name of file containing game data saved in JSON format
        number: integer
            max no. of valid games to retrieve; default is 10
        progress: boolean
            show which games are being retrieved
    """
    if not number:
        number = 10
    else:
        number = int(number)
    tmpdir = tempfile.mkdtemp()
    predictable_filename = 'bgggames.cache'
    dbname = os.path.join(tmpdir, predictable_filename)
    bgg = BoardGameGeek(cache="sqlite://{}?ttl=1000".format(dbname),
                        disable_ssl=True)
    games = []
    if user:
        ids = []
        #bgg_user = bgg.user(user)
        try:
            collection = bgg.collection(user)
            if collection:
                for game in collection:
                    ids.append(game.id)
            else:
                print 'Unable to retrieve collection for %s - do they exist?' \
                    % user
        except BoardGameGeekAPIRetryError, err:
            print err
    if filename:
        try:
            with open(filename) as json_file:
                json_games = json.load(json_file)
            for game_id in json_games.keys():
                games.append(GameObject(json_games[game_id]))
        except ValueError:
            print 'Unable to load data from "%s" - please check it.' % filename
    elif ids:
        count = 0
        for game_id in ids:
            if count >= number:
                break
            if progress:
                print "Retrieving game %7d from BGG !" % game_id
            _game = BGGGame(game_id=game_id)
            # TODO - find out a way to filter by user.owned ...
            flag = True
            if flag:
                games.append(_game)
                count += 1
    return games
