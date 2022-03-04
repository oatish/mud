import os
import sys
import pytest


def pytest_sessionstart(session):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


@pytest.fixture()
def module_extra():
    return os.path.join(os.path.dirname(__file__), "src/extra.py")


@pytest.fixture()
def module_simple():
    return os.path.join(os.path.dirname(__file__), "src/simple.py")
