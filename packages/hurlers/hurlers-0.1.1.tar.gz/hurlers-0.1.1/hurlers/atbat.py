from bs4.element import Tag as ELEMENT_TAG 
from bs4 import BeautifulSoup as BS
from .pitch import Pitch
from .runner import Runner

class AtBat(object):
    """
    Store atbat data.
    """
    AB_ATTRS = set([
      'away_team_runs',
      'b',
      'b_height',
      'batter',
      'des',
      'des_es',
      'earned', 
      'end_tfs_zulu',
      'event',
      'event2',
      'event_es',
      'event_num',
      'gid',
      'home_team_runs',
      'inning',
      'num',
      'o',
      'p_throws',
      'pitcher',
      'play_guid',
      'rbi',
      's',
      'score',
      'stand',
      'start_tfs',
      'start_tfs_zulu'
    ])

    IGNORE = set()

    def __init__(self, xml, **kwargs):
        """
        Params
        ------
        xml : string | bs4.element.Tag instance 
        """

        ## soupify if not soupified
        atbat_tag = xml if type(xml) == ELEMENT_TAG else BS(xml, "lxml").find("atbat")
        self.atbat_tag = atbat_tag

        ## store each attribute on the 'atBat' tag
        for attr in atbat_tag.attrs:
            if attr in AtBat.AB_ATTRS:
                self.__dict__[attr] = atbat_tag[attr]
            else:
                self.__dict__[attr] = atbat_tag[attr]

        ## store user defined data
        for attr in kwargs:
            if attr in AtBat.AB_ATTRS:
                self.__dict__[attr] = kwargs[attr]
            else:
                if attr not in AtBat.IGNORE:
                    self.__dict__[attr] = kwargs[attr]
        
        ## map 'runner' tags to Runner instances 
        self._runners = map(Runner, atbat_tag.find_all("runner"))

        ## preprocessing for storing pitches
        self._pitch_tags = atbat_tag.find_all("pitch") 
        self._store_pitch_type_sequence_and_type_sequence()
        keywords = {
            'pitcher': self.pitcher,
            'batter':  self.batter,
            'start_tfs_zulu': self.start_tfs_zulu,
            'end_tfs_zulu': self.end_tfs_zulu,
            'inning': self.inning,
            'gid': self.gid
        }

        ## map 'pitch' tags to Pitch instances 
        self._pitches = map(lambda t: Pitch(t, **keywords), self._gen_pitches())

    ## FIXME adding attributes to pitches this way is hacky but fine for now; it
    ## is assumed that most features will be developed post processing, but if
    ## that changes, adding features to pitches based on existing features should
    ## be easier/cleaner
    def _gen_pitches(self):
        """
        Generator of extended 'pitch' tags. 
        """
        i = 0 
        pitches = self.atbat_tag.find_all("pitches") 
        while i < len(self._pitch_tags):
            p = self._pitch_tags[i]

            p.attrs['pitch_no'] = i+1
            p.attrs['type_sequence'] = self._type_sequence
            p.attrs['pitch_type_sequence'] = self._pitch_type_sequence 
            p.attrs['event'] = self.atbat_tag.get("event") 
            yield p
            i+=1

    ## REQUIRES self._pitch_tags to be defined
    def _store_pitch_type_sequence_and_type_sequence(self):
        self._pitch_type_sequence, self._type_sequence = [], []
        for p in self._pitch_tags:
            self._pitch_type_sequence.append(p.get("pitch_type"))
            self._type_sequence.append(p.get("type"))
            

