import os
import shutil
import subprocess
import sys

from jill.install import install_julia

script_dir = os.path.dirname(os.path.realpath(__file__))

def _find_julia():
    # TODO: this should probably fallback to query jill
    return shutil.which("julia")


def install(*, confirm=False):
    """
    Install Julia (if required) and Julia packages required for dojopy.
    """
    julia = _find_julia()
    if julia:
        print("█████ stage 1 - a version of Julia has been found, we skip the installation of Julia")
    else:
        print("█████ stage 1 - no Julia version found, installing Julia")
        install_julia(confirm=confirm)
        julia = _find_julia()
        if not julia:
            raise RuntimeError(
                "Julia installed with jill but `julia` binary cannot be found in the path"
            )
    env = os.environ.copy()
    print("█████ stage 2 - set environment variable PYTHON to ", sys.executable)
    env["PYTHON"] = sys.executable
    # this call the script add_julia_packages.jl contained in this scripts' directory
    print("█████ stage 3 - add Julia packages: PyCall, Dojo -- build PyCall -- compile PyCall and Dojo")
    subprocess.check_call([julia, os.path.join(script_dir, "add_julia_packages.jl")], env=env)

install()
