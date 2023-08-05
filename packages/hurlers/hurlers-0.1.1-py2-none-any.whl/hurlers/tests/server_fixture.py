import pytest
import subprocess
import requests
import time 
import os

## start a simple http server that serves xml
@pytest.fixture(scope="module")
def server(request):
    import os
    port = 5555
    url = "http://localhost:{}".format(port)
    p = subprocess.Popen(
      ["python", "-m", "SimpleHTTPServer", str(port)], 
      stdout=subprocess.PIPE,
      cwd=find_xml_dir(os.getcwd()))

    attempts = 10
    while attempts > 0: 
        try:
            r = requests.get(url)
            attempts = 0
        except requests.exceptions.ConnectionError as e:
            attempts -= 1
            time.sleep(1/2.)

    def teardown():
        p.kill()

    request.addfinalizer(teardown)
    return url

def find_xml_dir(path):
    if os.path.basename(path) == 'xml':
        return path 

    for root, dirs, files in os.walk(path):
        if 'tests' in dirs:
            return find_xml_dir(os.path.join(path, 'tests'))
        elif 'hurlers' in dirs:
            return find_xml_dir(os.path.join(path, 'hurlers'))
        elif 'xml' in dirs:
            return find_xml_dir(os.path.join(path, 'xml'))
