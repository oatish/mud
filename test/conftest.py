import os
import sys
import pytest


@pytest.fixture()
def module_extra():
    return os.path.join(os.path.dirname(__file__), "mud/extra.pyfake")


@pytest.fixture()
def module_simple():
    return os.path.join(os.path.dirname(__file__), "mud/simple.pyfake")
