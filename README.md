# Python interface for Dojo.jl

This is a thin Python-wrapper around the Julia package [Dojo.jl](https://github.com/simon-lc/Dojo.jl). 

## Installation
1. Install this package: `git clone https://github.com/simon-lc/dojopy` (for now, later via pip / conda)

The wrapper makes a call to Julia via the pyjulia interface. To set this up:

2. Install  [`pyenv`](https://julialang.org/downloads/)
    - Installation guide for [Ubuntu](https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/)
    - Installation guide for [MacOS](https://julialang.org/downloads/)
    - Installation guide for [Windows](https://julialang.org/downloads/)

3. Use `pyenv` to [build your own Python](https://pyjulia.readthedocs.io/en/stable/troubleshooting.html#ultimate-fix-build-your-own-python)
    In `~/.pyenv` run: `PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.6` to create a custom binary.
    - We call this python binary the `custom_python`. It's located at `path/to/custom_python` e.g. `/home/user/.pyenv/versions/3.6.6/bin/python3` 
    - This step is needed because PyJulia cannot be initialized properly out-of-the-box when Python executables are statically linked to libpython. This is the case if you use Python installed with Debian-based Linux distribution such as Ubuntu or installed Python via conda. More details about this [here](https://pyjulia.readthedocs.io/en/stable/troubleshooting.html#ultimate-fix-build-your-own-python).

4. (Optional) Create a virtual environment linked to `custom_python`
    - In your shell run: `path/to/custom_python -m venv /path/to/new/virtual/environment/my_env`

**On the Julia side:**

5. Install the *Julia* programming language (`v1.5+` recommended) [[Julia Download page]](https://julialang.org/downloads/)

6. Install [`PyCall`](https://github.com/JuliaPy/PyCall.jl)
     - [Specify the Python version](https://github.com/JuliaPy/PyCall.jl#specifying-the-python-version) to be the `custom_python`.
     - e.g. `ENV["PYTHON"] = "/home/user/.pyenv/versions/3.6.9/bin/python3"`
     - `Pkg.build("PyCall")`
   
7. Open the Julia REPL and install the Julia package `Dojo.jl`: `(type ])`: 
```julia
pkg> add https://github.com/simon-lc/Dojo.jl
```

**On the Python side:**

8. In your virtual environment, install: `pyjulia`, the interface that lets you call Julia code from Python: 
    - Activate your virtual environement, then run
    - `python3 -m pip install julia` 

9. In Python run `import julia` followed by `julia.install()` to finish the `pyjulia` setup.

## Documentation
These notes only refer to the usage of this interface. For a more general overview take a look at the [Documentation](https://github.com/simon-lc/Dojo.jl) of the Julia package.

## Performance
We advise to read the [Performance Tips](https://github.com/simon-lc/Dojo.jl) page. In particular, when Dojo is called from a python script, e.g. `python3 ...` Julia will *just-in-time* compile the solver code which will slow down the overall execution. For larger problems it is advisable to solve a mini problem first to trigger the JIT-compilation and get full performance on the subsequent solve of the actual problem .

## Licence
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
