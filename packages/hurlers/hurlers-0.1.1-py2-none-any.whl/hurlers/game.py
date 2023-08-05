import time
import os
import datetime
from bs4 import BeautifulSoup as BS
from bs4.element import Tag as ELEMENT_TAG
from bs4 import BeautifulSoup as BS
from .utils.url_utils import *
from .utils.soup_utils import *
from .utils.csv_utils import *
from .inning import Inning
from .player import Player

class Game(object):
    """
    Get all the game data for a game id url.
    """

    GAME_ATTRS = set([
      "local_game_time",
      "game_pk",
      "game_time_et",
      "gameday_sw",
      "type"
    ])

    def __init__(self, gid_url):
        """
        Params
        ------
        gid_url : string
            gameday id url or gameday id directory

        """

        self._gid_url = gid_url
        self._gid = url_to_gid(gid_url)
        self._gidisdir = os.path.isdir(gid_url)
        if self._gidisdir: print "[XML ON DISK] stored @ {}".format(gid_url)

        ## convert gid to inning and player urls
        self._game_url = url_gid_to_game(gid_url)
        self._inning_all_url = url_gid_to_inning(gid_url, isfile=self._gidisdir)
        self._players_url = url_gid_to_players(gid_url)

        ## try to get the data over the network if the XML isn't on disk and
        ## soupify
        if self._gidisdir:
            with open(self._inning_all_url) as f:
                self._inning_all_soup = BS(f.read(), "lxml")
            with open(self._game_url) as f:
                self._game_soup = BS(f.read(), "lxml")
            with open(self._players_url) as f:
                self._players_soup = BS(f.read(), "lxml")
        else:
            self._inning_all_soup = GET_page_soup(self._inning_all_url)
            self._game_soup = GET_page_soup(self._game_url)
            self._players_soup = GET_page_soup(self._players_url)

        ## FIXME ugly
        self.successful_xml_retrieval = True

        ## unicode for printing to unicode enabled outputs
        telescope = u"\U0001f52d"
        thumbsup = u"\U0001f44d"
        try:
            print telescope +"  "+self._gid
        except:
            print "[PARSING] {}".format(self._gid)

        # mark true so client can check if Game instance is valid
        ## TODO (see line ~51)
        if not self._inning_all_soup or not self._game_soup or not self._players_soup:
            print "[ERROR] Did not store data for gid: '{}'.".format(self._gid)
            self.successful_xml_retrieval = False
            return

        ## TODO need to abort if none of the pages were retrieved

        ## add attributes to instance
        game_tag = self._game_soup.find("game")
        for attr in game_tag.attrs:
            if attr in Game.GAME_ATTRS:
                self.__dict__[attr] = game_tag[attr]
            else:
                print "[WARNING] Unregistered game attribute '{}'".format(attr)

        self._team_tags = game_tag.find_all("team")
        self._home_tag = self._team_tags[0] if self._team_tags[0].get("type") == "home" else self._team_tags[1]
        self._away_tag = self._team_tags[0] if self._team_tags[0].get("type") == "away" else self._team_tags[1]
        self._stadium_tag = game_tag.find("stadium")
        self._pitch_tags = self._inning_all_soup.find_all("pitch")

        # convert inning and player soup to Inning and Player instances,
        # respectively
        if not self._inning_all_soup:
            print "[WARNING] no inning soup"
        self._innings = map(lambda i: Inning(i, gid=self._gid), self._inning_all_soup.find_all("inning"))
        self._players = map(Player, self._players_soup.find_all("player"))

        ## map ids to player instances
        self._player_map = {}
        for player in self._players:
          self._player_map[player.id] = player

        ## cache pitcher ids
        self._pitcher_ids = set()

        ## cache all pitches in game
        self._pitches = []

        try:
            print thumbsup + "  " + self.__str__() + "\n"
        except:
            print "[SUCCESS]" + "  " + self.__str__() + "\n"

    def __str__(self):
        return "{} vs {}".format(self._away_tag.get("name_full"), self._home_tag.get("name_full"))

    def _get_player_name(self, id):
        """
        Convert player id to '[first name] [last name]'.
        """
        id = str(id) if type(id) == int else id
        p = self._player_map[id]
        return p.first + " " + p.last

    def _store_pitcher_ids(self):
        for inning in self._innings:
            for atbat in inning._atbats:
                if atbat.pitcher not in self._pitcher_ids:
                    self._pitcher_ids.add(atbat.pitcher)

    def get_pitches(self):
        """
        All pitches in game.

        Returns
        -------
        list of Pitch instances
        """
        if not self._pitches:
            self._pitches = [pitch for inning in self._innings for atbat in inning._atbats for pitch in atbat._pitches]
        return self._pitches

    def get_pitchers(self):
        """
        Participating pitchers. Not in order.

        Returns
        -------
        list of Player instances.
        """
        if not self._pitcher_ids:
            self._store_pitcher_ids()
        return filter(lambda p: p.id in self._pitcher_ids, self._players)

    def get_pitcher_names(self):
        """
        Participating pitchers. Not in order.

        Returns
        -------
        list of strings.

        """
        if not self._pitcher_ids:
            self._store_pitcher_ids()
        return map(lambda id: "{} - ".format(id) + self._get_player_name(id), self._pitcher_ids)

    def print_pitchers(self):
        for name in self.get_pitcher_names():
            print name
