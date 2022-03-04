#!/bin/bash
set -x

# Run black to format all code
black mud
black tests

# Lint check
pylint mud --disable=C0301,C0114,C0116,W1514,C0103,E0401 --fail-under=10
pylint tests --disable=C0301,C0114,C0116,W1514,C0103,E0401,W0613,E0402 --fail-under=10

# Coverage check
coverage run -m pytest
coverage report --fail-under=75

# Type check
mypy mud --ignore-missing-imports