import pytest
import yaml
from importlib import invalidate_caches

tested_loggers = ['devconfig',]

@pytest.yield_fixture
def mocked_iterload(mocker):
    _load = yaml.load
    yaml.load = mocker.Mock()
    yield yaml.load 
    yaml.load = _load

@pytest.yield_fixture
def empty_yaml_open_file():
    with open('tests/samples/empty.yaml', 'r') as empty_yaml:
        yield empty_yaml


@pytest.yield_fixture(scope='function')
def uncached():
    invalidate_caches()
    yield None