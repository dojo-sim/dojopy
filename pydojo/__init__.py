import os
import subprocess
script_dir = os.path.dirname(os.path.realpath(__file__))

from dojopy.interface import *


# def install():
#     """
#     Install Julia packages required for cosmopy.
#     """
#     subprocess.check_call(['julia', os.path.join(script_dir, 'install.jl')])