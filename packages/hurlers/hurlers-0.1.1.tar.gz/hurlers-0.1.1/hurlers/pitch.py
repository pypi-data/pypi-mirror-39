import sqlite3
import datetime
from bs4.element import Tag as ELEMENT_TAG 

class Pitch(object):
    """
    Store pitch data.
    """
    PITCH_ATTRS = set([
      'ax',
      'ay',
      'az',
      'batter', 
      'break_angle',
      'break_length',
      'break_y',
      'cc',
      'code',
      'des',
      ### ignore spanish for now 'des_es', 
      'end_speed',
      'end_tfs_zulu',
      'event',
      'event_num',
      'gid',
      'id',
      'inning',
      'mt',
      'nasty',
      'on_1b',
      'on_2b',
      'on_3b',
      'pfx_x',
      'pfx_z',
      'pitch_no',
      'pitch_type',
      'pitch_type_sequence',
      'pitcher',
      'play_guid',
      'px',
      'pz',
      'spin_dir',
      'spin_rate',
      'start_speed',
      'start_tfs_zulu',
      'sv_id',
      'sz_bot',
      'sz_top',
      'tfs',
      'tfs_zulu',
      'type',
      'type_confidence',
      'type_sequence',
      'vx0',
      'vy0',
      'vz0',
      'x',
      'x0',
      'y',
      'y0',
      'z0',
      'zone'
    ]) 
    IGNORE = set(['des_es'])

    INTEGER = set([
      'inning',
      'pitch_no',
      'id',
      'zone',
      'tfs',
      'event_num',
      'pitcher',
      'batter',
      'nasty',
      'on_1b',
      'on_2b',
      'on_3b'
    ] )

    REAL = set([
      'spin_rate',
      'break_angle',
      'sz_top',
      'y0',
      'ay',
      'ax',
      'az',
      'end_speed',
      'spin_dir',
      'start_speed',
      'pz',
      'px',
      'pfx_z',
      'vy0',
      'pfx_x',
      'break_length',
      'z0',
      'break_y',
      'vz0',
      'x0',
      'type_confidence',
      'y',
      'x',
      'sz_bot',
      'vx0'
    ])

    TEXT = set([
      'pitch_type_sequence',
      'code',
      'cc',
      'pitch_type',
      'pitch_id',
      'play_guid',
      'event',
      'gid',
      'type',
      'start_tfs_zulu',
      'tfs_zulu',
      'end_tfs_zulu',
      'type_sequence',
      'des',
      'mt',
      'sv_id'
    ])

    def __init__(self, xml, **kwargs):
        """
        Params
        ------
        xml : string | bs4.element.Tag instance 

        Keyword Arguments
        -----------------
        home_tag : bs4.element.Tag instance
          home team soup tag

        away_tag : bs4.element.Tag instance
          away team soup tag

        stadium_tag : bs4.element.Tag instance
          stadium soup tag

        Attribute Key
        ------------
        'x': Point for X(inches)
        'y': Point for Y(inches)
        'start_speed': The pitch speed(MPH) at the initial point
        'end_speed': The pitch speed(MPH) at the current batters
        'sz_top': The distance in feet from the ground to the top of the current batter's
        'sz_bot': The distance in feet from the ground to the bottom of the current batter's
        'pfx_x': The horizontal movement, in inches, of the pitch between the release point and home plate
        'pfx_z': The vertical movement, in inches, of the pitch between the release point and home plate
        'px': The left/right distance, in feet, of the pitch from the middle of the plate as it crossed home plate
        'pz': The height of the pitch in feet as it crossed the front of home plate
        'x0': The left/right distance, in feet, of the pitch, measured at the initial point
        'y0': The distance in feet from home plate where the PITCHf/x system is set to measure the initial parameters
        'z0': The height, in feet, of the pitch, measured at the initial point
        'vx0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
        'vy0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
        'vz0': The velocity of the pitch, in feet per second, in three dimensions, measured at the initial point
        'ax': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
        'ay': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
        'az': The acceleration of the pitch, in feet per second per second, in three dimensions, measured at the initial point
        'break_y': The distance in feet from the ground to the top of the current batter's
        'break_angle': The angle, in degrees, from vertical to the straight line path from the release point to where the pitch crossed the front of home plate, as seen from the catcher's/umpire's perspective
        'break_length': The measurement of the greatest distance, in inches, between the trajectory of the pitch at any point between the release point and the front of home plate
        'pitch_type': Pitch Type
        'pitch_type_seq': Pitch type Sequence, ex:FF|CU|FF
        'type_confidence': Pitch type confidence
        'zone': Pitch Zone
        'spin_dir': Pitch Spin Dir
        'spin_rate': Pitch Spin Rate
        'sv_id': Pitch in the air(From Datetime_To Datetime)
        'event_num': Event Sequence Number(atbat, pitch, action)
        """

        self.home_tag    = home_tag    if "home_tag"    in kwargs else None
        self.away_tag    = away_tag    if "away_tag"    in kwargs else None
        self.stadium_tag = stadium_tag if "stadium_tag" in kwargs else None

        ## presence varies from tag to tag
        self.on_1b = None
        self.on_2b = None
        self.on_3b = None

        ## instantiate all attrs
        for attr in Pitch.PITCH_ATTRS: self.__dict__[attr] = None

        ## store data from xml
        self._pitch_tag = xml if type(xml) == ELEMENT_TAG else BS(xml, "lxml").find("pitch")
        for attr in self._pitch_tag.attrs.keys():
            if attr in Pitch.PITCH_ATTRS:
                self.__dict__[attr] = self._pitch_tag.get(attr)
            else:
               if attr not in Pitch.IGNORE: 
                    print "Unregistered pitch attribute '{}'".format(attr)

        for attr in kwargs:
            if attr in Pitch.PITCH_ATTRS:
                self.__dict__[attr] = kwargs[attr]
            else:
                if attr not in Pitch.IGNORE: 
                    print "Unregistered pitch keyword '{}'".format(attr)


    @classmethod
    def create_pitch_id(cls, tfs_zulu, pitcher, id):
        import hashlib
        return hashlib.md5(tfs_zulu + str(pitcher) + str(id)).hexdigest()
           
