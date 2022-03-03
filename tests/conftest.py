import os
import sys
import pytest


def pytest_sessionstart(session):
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))


@pytest.fixture()
def test_module():
    return os.path.join(os.path.dirname(__file__), "src/test.py")
