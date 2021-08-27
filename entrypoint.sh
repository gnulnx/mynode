#!/usr/bin/env bash

pip3 install -r requirements.txt
python3 backend/app.py

# Leave somethign running in case we need to get into the
# container to poke around
tail -f /dev/null
