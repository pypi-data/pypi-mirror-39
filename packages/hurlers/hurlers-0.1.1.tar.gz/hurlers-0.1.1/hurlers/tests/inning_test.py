import requests

from ..inning import Inning
from .server_fixture import server

def test_inning_raw_xml(server):
    gid = "gid_2018_03_27_anamlb_lanmlb_1"
    response = requests.get(server + "/inning.xml" )
    i = Inning(response.text, gid=gid)
    assert i.num == "1"
    assert i.next == "Y"
    assert i.away_team == "ana"
    assert i.gid == gid
    assert i.home_team == "lan"


