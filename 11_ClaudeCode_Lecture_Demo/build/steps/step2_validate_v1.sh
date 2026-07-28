#!/bin/bash
cd "$(dirname "$0")/.."
clear
echo "\$ python3 validate.py schedule_v1.json"
echo
python3 validate.py schedule_v1.json
