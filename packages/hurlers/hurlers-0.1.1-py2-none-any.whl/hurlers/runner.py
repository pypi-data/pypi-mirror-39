from bs4.element import Tag as ELEMENT_TAG 
from bs4 import BeautifulSoup as BS

class Runner(object):
    """
    Store runner data.
    """

    RUNNER_ATTRS = {
      'earned',
      'end',
      'event',
      'event_num',
      'id',
      'rbi',
      'score',
      'start'
    }
    def __init__(self, xml):
       """
       Params
       ---------
       xml : string | bs4.element.Tag
       """
       runner_tag = xml if type(xml) == ELEMENT_TAG else BS(xml, "lxml").find("runner")
       self.runner_tag = runner_tag
       for attr in runner_tag.attrs:
           if attr in Runner.RUNNER_ATTRS:
               self.__dict__[attr] = runner_tag[attr]
           else:
               print "[WARNING] Unregistered runner attribute '{}'".format(attr)
               self.__dict__[attr] = runner_tag[attr]

    
