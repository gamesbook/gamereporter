#!/usr/bin/env python
"""
Author: Derek Hohls
Date: June 2016
Purpose:
    Supply game-like objects that can be used to test GameReportBuilder without
    requiring access to boardgamegeek.com
"""

class Game(object):

    def __init__(self, item):
    
        self.id = item.get('id', 0)
        self.name = item.get('name', 'NAME?')
        self.description = item.get('desc', 'NAME?')
        self.description_html = item.get('desc', 'NAME?').\
            replace('[', '<').replace(']', '>').replace('\n', '<br/>')
        self.image = item.get('image', '')
        self.categories =  item.get('categories', '???')
        self.mechanics =  item.get('mechanics', '???')
        self.players =  item.get('players', '1-100')
        self.age =  item.get('age', '1+')
        self.yearpublished =  item.get('yearpublished', '0000')
        self.playingtime =  item.get('playingtime', '60')


# example games - ALL text and images sourced from http://www.boardgamegeek.com

game1 = {
'name': '1830',
'id': 421,
'image': 'dummy/1830.png',
'desc': """1830 is one of the most famous 18xx games. One of the things some gamers like about this game is that the game has 'no chance' element. That is to say, if players wished to play two games with the same moves, the outcome would be the same also.

This game takes the basic mechanics from Tresham's 1829, and adds several new elements. Players are seeking to make the most money by buying and selling stock in various share companies located on eastern United States map. The stock manipulation aspect of the game is widely-regarded as one of the best. The board itself is actually a fairly abstract hexagonal system, with track tiles placed on top of the hexes. Plus each 18xx title adds new and different elements to the game. This game features private rail companies and an extremely vicious, 'robber baron' oriented stock market. A game is finished when the bank runs out of money or one player is forced to declare bankruptcy, and the player with the greatest personal holdings wins.

The 2011 version of 1830 was published by Mayfair Games in partnership with Lookout Games of Germany. This publication was developed under license from Francis Tresham in co-operation with Bruce Shelley (the original 1830 developer). This version contains rules and components for Francis Tresham's original classic design, a faster-playing basic game, and new variants from some of the world's best railroad game developers.""",
'categories': 'Economic, Trains, Transportation',
'mechanics': 'Auction/Bidding, Route/Network Building, Stock Holding, Tile Placement',
'players': '2-5',
'age': '12+',
'yearpublished': '1986',
'playingtime': '240'}

game2 = {
'name': 'Babel',
'id': 986,
'image': 'dummy/babel.png',
'desc': """In Babel, each player makes use of members of various tribes of the ancient world to build temples, exploit (or exterminated) their opponent's work force, destroy or steal their opponent's temples and otherwise do whatever it takes to build the tallest temples to win the game.

The game plays out on a small game board representing regions of 5 ancient civilizations, Medes, Sumerians, Hitites, Persians, and Assyrians. Each player will be dealt a hand of cards (consisting of 5 types corresponding to the above tribes). Players themselves are represented by stone figures. Temple cards will be made available at the side of the board for building throughout the game. On his or her turn, a player may discard a card to move to the corresponding region, place a card on the region they are currently located, build a temple by having tribesmen equal to the number or level on the temple card AND having built the previous (lower) temple level, move tribesmen from one region to another, or perform a skill action unique to each tribe. Players may perform any and all actions available to them, being able to perform most actions as many times as they wish and saving any number of unplayed cards for subsequent turns.

A [b]big[/b] component of this game is placing your tribe cards in sets. Skills can only be used if a set of three (or more) cards is at the same location as the player marker. By discarding one of the cards of a set, the skill may be used. No matter the tribe, performing this action can force the opponent to discard half their hand. Other skills, such as robbing a temple from an opponent, skipping a level on a temple build, destroy an opposing temple, etc. are specific to the tribe activated.

Game play progresses until one of two conditions is met: if a player builds 15 points (or levels) of temples before the opposing player builds at least 10 points, that player wins. If the opponent [i]does have[/i] more than 10 points, the game continues until one player reaches 20 points (in which case he or she wins) OR one player subsequently drops below 10 (in which case he or she loses).""",
'categories': 'Ancient, Card Game, City Building',
'mechanics': 'Hand Management, Set Collection',
'players': '2-4',
'age': '10+',
'yearpublished': '2012',
'playingtime': '45'}

game3 = {
'name': '7 Wonders: Babel',
'id': 154638,
'image': 'dummy/babel7.png',
'desc': """[i]7 Wonders: Babel[/i] includes two modules for use with the 7 Wonders base game, and they can be used individually or together in any combination with other expansions. 

In one half of [i]7 Wonders: Babel[/i], players draft quarter-circle tiles at the start of the game prior to drafting anything else; each tile depicts a law that affects all players should it be put into play, e.g., all single resource cards provide an infinite number of resources each turn, or winners in military conflicts receive fewer points than normal. 

During the game, players now have an additional option when discarding a card. Instead of gaining three coins, they place one of these tiles in the next open space on a circular display; the law on this tile remains in effect until the end of the game or until it's covered. (Should a fifth tile be placed, for example, it's placed on top of the first tile played.) At the end of the game, players receive points based on how many tiles they played. 

In the second half of [i]7 Wonders: Babel[/i], one of five age specific great project cards is randomly revealed at the start of each age, and a number of tokens are placed on it, based on the number of players. This card imposes a tax on players who want to play cards of a certain color. When a player pays this tax, he takes one of the tokens from this law card. At the end of the age, if all of the tokens have been removed, then players receive a bonus (which is depicted on the card) for each token they have; if tokens remain on the card, then each player without a token is penalized. 

Just as the cost of cards increases in each age, the number of resources required to pay the tax also increases.""",
'categories': 'Ancient, Card Game, City Building',
'mechanics': 'Hand Management, Set Collection',
'players': '2-2',
'age': '10+',
'yearpublished': '2015',
'playingtime': '30'}

games = [game1, game2, game3]

def get_games():
    items = []
    for game in games:
        dummy = Game(game)
        items.append(dummy)
    return items        

