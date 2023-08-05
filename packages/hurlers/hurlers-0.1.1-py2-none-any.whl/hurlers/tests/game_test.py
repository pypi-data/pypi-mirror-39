import requests

from ..game import Game

from .server_fixture import server

def test_game(server):
    gid = "gid_2018_10_28_bosmlb_lanmlb_1"
    g = Game(server + "/" + gid)

    pitcher_ids = set([
        '523260',
        '445276',
        '477132',
        '519242',
        '456034',
        '520980'
    ])

    pitchers = g.get_pitchers()

    assert len(pitchers) == len(pitcher_ids) 
    for pitcher in pitchers:
        assert pitcher.id in pitcher_ids
