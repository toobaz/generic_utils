"""
Convenience function to send an alert, based on an existing script.
The path of the script must be indicated below.
It must accept as argument a text, and do with it whatever is required (e.g.
send a Telegram message to a predefined account/group).
"""
import os

from pathlib import Path
home = str(Path.home())

SCRIPT_PATH = f'{home}/bin/warnme.py'

from datetime import datetime
import subprocess

def doner(msg=''):
    print("Done at", datetime.now().strftime("%Y-%m-%d %H:%M"))
    if not os.path.exists(SCRIPT_PATH):
#        print("Warning - {SCRIPT_PATH} does not exist")
        return
    subprocess.call([SCRIPT_PATH, str(msg)])
