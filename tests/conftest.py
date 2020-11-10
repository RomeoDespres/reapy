import pathlib
import subprocess
import time

import pytest

import reapy


@pytest.fixture(scope='session', autouse=True)
def reaper(request):
    reaper_command = pathlib.Path(__file__).parent / 'reaper' / 'reaper.exe'
    process = subprocess.Popen(str(reaper_command))
    trials = 0
    while not reapy.dist_api_is_enabled():
        if trials == 10:
            raise RuntimeError('reapy could not connect.')
        time.sleep(1)
        reapy.reconnect()
        trials += 1
    request.addfinalizer(process.terminate)
