import os
import pathlib
import shutil
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

    def finalizer():
        reapy.open_project('')
        process.terminate()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='session')
def temp_projects_dir(request):
    temp_projects_dir = pathlib.Path(__file__).parent / 'temp_projects'
    os.mkdir(temp_projects_dir)
    request.addfinalizer(lambda: shutil.rmtree(temp_projects_dir))
    return temp_projects_dir


def open_project(name, request, temp_projects_dir):
    name += '.rpp'
    source = pathlib.Path(__file__).parent / 'projects' / name
    destination = pathlib.Path(__file__).parent / temp_projects_dir / name
    shutil.copy(source, destination)
    project = reapy.open_project(str(destination))
    request.addfinalizer(project.save)
    return project


def inject_project_fixture(name, mutable):

    @pytest.fixture(scope='function' if mutable else 'session')
    def project(reaper, temp_projects_dir, request):
        return open_project(name, request, temp_projects_dir)

    fixture_name = ('' if mutable else 'im') + f'mutable_{name}_project'
    globals()[fixture_name] = project


for path in (pathlib.Path(__file__).parent / 'projects').iterdir():
    for mutable in True, False:
        inject_project_fixture(path.name[:-4], mutable)
