import requests

from ..atbat import AtBat
from .server_fixture import server

def test_atbat_raw_xml(server):
    gid = "gid_2018_03_27_anamlb_lanmlb_1"
    inning = 1
    response = requests.get(server + "/atbat.xml" )
    a = AtBat(response.text, gid=gid, inning=1)

    assert a.gid == gid
    assert a.inning == 1 
    assert a.away_team_runs == "0"
    assert a.b == "2"
    assert a.b_height == "6-0"
    assert a.batter == "446359"
    assert a.des == "Zack Cozart lines out sharply to left fielder Matt Kemp.  " 
    assert a.end_tfs_zulu == "2018-03-28T02:11:52Z" 
    assert a.event == "Lineout" 
    assert a.event_num == "10" 
    assert a.home_team_runs == "0" 
    assert a.num == "1" 
    assert a.o == "1" 
    assert a.p_throws == "L" 
    assert a.pitcher == "547943" 
    assert a.play_guid == "3ee5fe7a-29fc-421e-adec-5629aaa796c3" 
    assert a.s == "2" 
    assert a.stand == "R" 
    assert a.start_tfs == "030915" 
    assert a.start_tfs_zulu == "2018-03-28T03:09:15Z"

def test_atbat_raw_xml_pitch_type_sequence(server):
    gid = "gid_2018_03_27_anamlb_lanmlb_1"
    inning = 1
    response = requests.get(server + "/atbat.xml" )
    a = AtBat(response.text, gid=gid, inning=1)
    assert a._pitch_type_sequence == ['FF', 'FC', 'CU', 'FF', 'CU', 'FF']
