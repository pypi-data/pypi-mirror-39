from __future__ import print_function

import sys
import datetime
import requests
import re
from bs4 import BeautifulSoup as BS
from .constants import GID_P

def GET_page_soup(url):
    """
    Get and soupify the text at a url.    

    Params
    ------
    url : string
      Expects properly formatted URI.

    Note
    ----
    Methods that start with 'GET', make a network request.

    Returns
    -------
    If request is OK, returns soup of text. Else prints error code and returns
    `None`.
    """

    # grab the gameday id bits from the full url
    gid_match = re.search(GID_P, url)

    try: 
        response = requests.get(url, timeout=3)
    except (requests.ConnectionError, requests.Timeout) as e:
        ## FIXME not tested well
        if type(e) == requests.ConnectionError:
            print("[ERROR] Could not connect to '{}'".format(url), file=sys.stderr)
        else:
            print("[TIMEOUT] No response from '{}'.".format(url), file=sys.stderr)
        return

    status_is_ok = response.status_code >= 200 and response.status_code < 300
    if response.ok and status_is_ok:
        return BS(response.text, features="xml") 
    else:
        print("[ERROR] Bad response from {}. CODE: {}".format(url, str(response.status_code)), file=sys.stderr)
        return
