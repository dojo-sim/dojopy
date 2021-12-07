# import julia
# julia.install()

# from julia.api import Julia
# jl = Julia(compiled_modules=False)

from julia import Base

Base.sind(90)

import julia.Base
from julia.Base import Enums    # import a submodule
from julia.Base import sin      # import a function from a module

from julia import Main
Main.xs = [1, 2, 3]

a = Main.eval("sin.(xs)")
print(a)

from julia import LinearAlgebra as _LinearAlgebra
b = Main.eval("LinearAlgebra.zeros")
print(b)

from julia import Dojo as _Dojo
b = Main.eval("Dojo.controldim")
print(b)


# install pyenv 
    # https://github.com/pyenv/pyenv
    # for ubuntu: https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/

# install your own version of python with shared lib_python using pyenv
    # Ultimate fix: build your own Python
    # https://pyjulia.readthedocs.io/en/stable/troubleshooting.html
    # we call this python binary the 'custom python'

# create a python virtualenv linked to the custom python you've just installed, we call this env the 'custom env'
    # path/to/custom_python -m venv /path/to/new/virtual/environment


# install julia 
    # install PyCall
    # Set the PYTHON env variable to your custom python
    # build PyCall

# in your custom env
    # install pyjulia
    # https://pyjulia.readthedocs.io/en/stable/installation.html

# now you can run a demo script in python calling your julia package
    # demo.py