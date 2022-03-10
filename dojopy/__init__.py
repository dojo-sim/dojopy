import os
import shutil
import subprocess
import sys

from os.path import dirname, abspath, join

def install(ENV_DIR="", *, confirm=False):
    """
    Install Julia (if required) and Julia packages required for dojopy.
    """
    print("█████------------------------------------------------------")
    print("█████ dojopy installation: this process may take up to 20 minutes on the first time.")
    print("█████------------------------------------------------------")
    WORKING_DIR = dirname(dirname(abspath(__file__)))
    FILE_DIR = dirname(abspath(__file__))
    p = subprocess.Popen(
        ["sudo", "bash", join(FILE_DIR, "install_dojopy.bash"), WORKING_DIR, ENV_DIR],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True)
    while True:
        line = p.stdout.readline()
        print(line.rstrip("\n"))
        if not line: break
