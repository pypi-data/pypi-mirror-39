from bs4.element import Tag as ELEMENT_TAG 
from bs4 import BeautifulSoup as BS
from .atbat import AtBat

class Inning(object):
    """
    Store inning data.
    """

    INN_ATTRS = set([ 
      "num",
      "next",
      "away_team",
      "gid",
      "home_team",
    ])
  
    def __init__(self, xml, **kwargs):
        """
        Params
        ------
        xml : string | bs4.element.Tag instance 
        """
        inning_tag = xml if type(xml) == ELEMENT_TAG else BS(xml, "lxml").find("inning")
        self.inning_tag = inning_tag
        for attr in inning_tag.attrs:
            if attr in Inning.INN_ATTRS:
                self.__dict__[attr] = inning_tag[attr]
            else:
                self.__dict__[attr] = inning_tag[attr]

        for attr in kwargs:
            if attr in Inning.INN_ATTRS:
                self.__dict__[attr] = kwargs[attr]
            else:
                self.__dict__[attr] = inning_tag[attr]

        top = inning_tag.find("top")
        bottom = inning_tag.find("bottom")

        self._top_atbats = map(lambda ab: AtBat(ab, gid=self.gid, inning=self.num), top.find_all("atbat")) if top else []
        self._bottom_atbats = map(lambda ab: AtBat(ab, gid=self.gid, inning=self.num), bottom.find_all("atbat")) if bottom else []
        self._atbats = self._top_atbats + self._bottom_atbats

