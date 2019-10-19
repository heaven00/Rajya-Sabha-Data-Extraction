#!/bin/sh

set -e

flake8 . --select C,E,F,W --show-source --statistics --max-complexity=10 --statistics
