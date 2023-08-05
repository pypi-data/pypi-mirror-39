from __future__ import print_function

import sys
import os
import re
from bs4 import BeautifulSoup as BS
from .soup_utils import GET_page_soup
from .constants import *

def url_date_to_gameday(day):
    """
    Generate a gameday url from a datetime object.
    
    Params
    ------
    day : datetime.datetime
      year, month, and day required

    Returns
    -------
    String representing url for retrieving gameday xml.
    """
    try:
        year   = "year_{}".format(str(day.year))
        month  = "month_{}".format(str(day.month).zfill(2))
        day    = "day_{}".format(str(day.day).zfill(2))
    except AttributeError as e:
        print("[ERROR] Requires a datetime.datetime object. You passed a {}".format(type(day)), file=sys.stderr)
        return

    return MLBBASEURL +"/".join([year, month, day]) 

def url_to_gid(url):
    """
    Grab the gid from the gameday url. 
    
    Params
    ------
    url : str

    Returns
    -------
    String representing gameday id.
    """
    match = re.search(GID_P, url)
    if match:
        return url[match.start():match.end()]
    else:
        print("[ERROR] Could not find gid in '{}'".format(url), file=sys.stderr)
    return url


def url_gid_to_inning(gameday_url, inning="all", isfile=False):
    """
    Convert a gameday url to an inning url.

    Params
    ------
    gameday_url : string 
      (see Format in `GET_gid_urls`)
    inning : string
      1-9, all

    Returns
    -------
    Returns a url string to from which inning xml can be retrieved.
    """
    if isfile:
        return os.path.join(gameday_url, "inning_{}.xml".format(inning))
    else:
        return os.path.join(gameday_url, "inning", "inning_{}.xml".format(inning))

def url_gid_to_players(gameday_url, inning="all"):
    """
    Convert a gameday url to an inning url.

    Params
    ------
    gameday_url : string 
      (see Format in `GET_gid_urls`)
    inning : string
      1-9, all

    Returns
    -------
    Returns a url string to from which inning xml can be retrieved.
    """
    return os.path.join(gameday_url,"players.xml")

def url_gid_to_game(gid_url):
    """
    Convert a gid url to a game xml url

    Params
    ------
    gid_url : string 
      (see Format in `GET_gid_urls`)
    inning : string
      1-9, all

    Returns
    -------
    Returns a url string to from which inning xml can be retrieved.
    """
    return os.path.join(gid_url,"game.xml")

def soup_get_game_tags(game_soup):
    """
    Find the game links in a soup object.

    Params
    ------
    soup : bs4.BeautifulSoup object

    Returns
    -------
    A list of tags.

    """
    return game_soup.find_all('a', href=re.compile(GID_P))


def GET_gid_urls(day):
    """
    Retrieve the gameday urls. 

    Params
    ------
    day : datetime.datetime object

    Note
    ----
    Methods that start with GET, make a network request.

    Returns
    -------
    List of strings. Format `gid_{yyyy}_{mm}_{dd}_{awy}{lgu}_{hom}{lgu}_1`.
    'yyyy' : four digit year
    'mm' : two digit month
    'dd' : two digit day
    'awy': three letter abbreviation for away team
    'hom': three letter abbreviation for home team
    'lgu': three letter abbreviation for league

    """
    gameday_url = url_date_to_gameday(day)
    soup = GET_page_soup(gameday_url)
    if soup:
        gamehrefs = soup_get_game_tags(soup)
        return map(lambda tag: gameday_url + "/" + tag.contents[0].strip(), gamehrefs)   
    return []

## TODO clean this up and move to util package
def has_game(gid_url):
    GAME    = 0 ## 0x1
    PLAYERS = 0 ## 0x2
    INNING  = 0 ## 0x4
    soup = GET_page_soup(gid_url)
    for tag in soup.find_all('a'):
        href = tag.get('href')
        if re.match('.*game.xml$', href):    GAME    = 0x1 
        if re.match('.*players.xml$', href): PLAYERS = 0x2 
        if re.match('.*inning\/$', href):    INNING  = 0x4 
    return (GAME | PLAYERS | INNING) == 0x7

