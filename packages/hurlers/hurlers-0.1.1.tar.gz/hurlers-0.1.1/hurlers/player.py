from bs4.element import Tag as ELEMENT_TAG 
from bs4 import BeautifulSoup as BS


class Player(object):
  """
  Store player data.
  """

  IN_GAME_ATTRS = set(['bat_order', 'current_position', 'game_position'])
  PITCHER_ATTRS = set(['era', 'losses', 'wins'])
  COMMON_ATTRS = set([
     'avg',
     'bats',
     'boxname',
     'first',
     'hr',
     'id',
     'last',
     'num',
     'parent_team_abbrev',
     'parent_team_id',
     'position',
     'rbi',
     'rl',
     'status',
     'team_abbrev',
     'team_id'
  ])

  def __init__(self, xml=""):
      """
      Params
      ------
      xml : string | bs4.element.Tag instance
        Expects a single player tag.
      """
      player_tag = xml if type(xml) == ELEMENT_TAG else BS(xml, "lxml").find("player")

      self.in_game = False
      self.is_pitcher = False
      self.player_tag = player_tag

      for attr in player_tag.attrs:
          if attr in Player.COMMON_ATTRS:
              self.__dict__[attr] = player_tag[attr]
          elif attr in Player.PITCHER_ATTRS:
              self.is_pitcher = True 
              self.__dict__[attr] = player_tag[attr]
          elif attr in Player.IN_GAME_ATTRS:
              self.in_game = True
              self.__dict__[attr] = player_tag[attr]

  def get_id(self):             return int(self.id)
  def get_formatted_name(self): return self.first + " " + self.last

