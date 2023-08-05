import requests

from bs4 import BeautifulSoup as BS

from ..runner import Runner
from .server_fixture import server


def test_runner_raw_xml(server):
    response = requests.get(server + "/runners.xml" )
    r = Runner(response.text)

    assert r.start == ""
    assert r.end == "1B"
    assert r.id == "645277"
    assert r.event == "Single"
    assert r.event_num == "10"

def test_runner_bs(server):
    response = requests.get(server + "/runners_bs.xml" )
    r = Runner(BS(response.text, "lxml").find("runner"))

    assert r.start == ""
    assert r.end == "1B"
    assert r.id == "645277"
    assert r.event == "Single"
    assert r.event_num == "10"
