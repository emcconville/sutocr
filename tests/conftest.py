from py.path import local
from pytest import fixture

@fixture
def sutocr_assets():
    return local(__file__).dirpath('assets')