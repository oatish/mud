#!/bin/bash

black src
black tests
coverage run -m pytest
coverage report --fail-under=75
mypy src