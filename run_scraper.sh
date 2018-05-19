#!/usr/bin/env bash

if [[ ! -d ".venv" ]];then
    python3.6 -m venv .venv > /dev/null
    source .venv/bin/activate
    sudo pip3 install -q -r requirements.txt > /dev/null
fi

source .venv/bin/activate

python3.6 scraper.py $1
