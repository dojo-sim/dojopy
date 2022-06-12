# Python interface for Dojo

This package is a Python wrapper for the differentiable simulator [Dojo](https://github.com/dojo-sim/Dojo.jl).
- arXiv preprint: https://arxiv.org/abs/2203.00806
- site: https://sites.google.com/view/dojo-sim
- video presentation: https://youtu.be/TRtOESXJxJQ

Included are interfaces to [PyTorch](https://github.com/pytorch/pytorch) and [JAX](https://github.com/google/jax).

## Quickstart 
This example simulates a pendulum for 1 time step.
```python
import dojopy 
from julia import Base
from julia import Dojo as dojo

# get an environment
env = dojo.get_environment('pendulum')
dojo.initialize_pendulum_b(env.mechanism, angle=0.0, angular_velocity=0.0)

# get state
x1 = dojo.get_minimal_state(env.mechanism)

# random control
u1 = Base.rand(nu)

# simulate one time step
dojo.step(env, x1, u1)
```

## Installation
Using `Dojo` with Python requires a number of installations in addition to `dojopy`. Below are two options for installing all dependencies.


### Using Docker (recommended)
1. Clone this repository: 

```bash
git clone https://github.com/dojo-sim/dojopy
```

2. Install Docker (https://docs.docker.com/engine/install/)

3. Enter the repository folder, build the Dockerfile and tag the image as `dojopy`: (this step may take a few minutes)

```bash
cd dojopy
docker build --tag dojopy .
```

4. Open a bash shell in your Docker container
```bash
docker run -it -v /absolute/path/to/dojopy:/dojopip dojopy bash
```
(`-v /absolute/path/to/dojopy:/dojopip` allows you to synchronize files from your folder `/absolute/path/to/dojopy` to your docker image)


5. You can now run dojopy inside your Docker image!
Inside the shell of your Docker image opened in step 4., run
```bash
python3 quick_start.py
```

### Manual (advanced)
Calling Dojo from Python requires: 
- dojopy: this wrapper
- Julia v1.6+
- Dojo.jl: the actual simulator
- PyCall: interface between Julia and Python 
- custom Python binary: this is required to make calls to Dojo fast and efficient 

Below we walk through each of the required installation steps: 

**Get `dojopy`**
1. Clone this repository: 

```bash
git clone https://github.com/dojo-sim/dojopy
```
(for now, soon via pip)

**Custom Python installation**
To make calls from Python to `Dojo` efficient requires a custom Python installation. 

2. Install `pyenv`
    - Installation guide for [Ubuntu](https://www.liquidweb.com/kb/how-to-install-pyenv-on-ubuntu-18-04/)
    - Installation guide for [MacOS](https://binx.io/blog/2019/04/12/installing-pyenv-on-macos/)
    - Installation guide for [Windows](https://github.com/pyenv-win/pyenv-win)

3. Use `pyenv` to [build your own Python](https://pyjulia.readthedocs.io/en/stable/troubleshooting.html#ultimate-fix-build-your-own-python)
    
    In `~/.pyenv` run: 

    ```bash
    PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.6.6
    ```

    to create a custom binary.

    - We call this python binary the `custom_python`. It's located at `path/to/custom_python` e.g., `/home/user/.pyenv/versions/3.6.6/bin/python3` 
    - This step is needed because PyJulia cannot be initialized properly out-of-the-box when Python executables are statically linked to libpython. This is the case if you use Python installed with Debian-based Linux distribution such as Ubuntu or installed Python via conda. More details about this [here](https://pyjulia.readthedocs.io/en/stable/troubleshooting.html#ultimate-fix-build-your-own-python).

4. (Optional, Recommended) Create a virtual environment linked to `custom_python`
    - In your shell run: 

    ```bash
    path/to/custom_python -m venv /path/to/new/virtual/environment/my_env
    ```

**Julia installation**

5. Install the *Julia* programming language (`v1.6+` recommended) [[Julia Download page]](https://julialang.org/downloads/)

6. Install [`PyCall`](https://github.com/JuliaPy/PyCall.jl)
     - [Specify the Python version](https://github.com/JuliaPy/PyCall.jl#specifying-the-python-version) to be the `custom_python`.
        - e.g. `ENV["PYTHON"] = "/home/user/.pyenv/versions/3.6.6/bin/python3"`
        - `Pkg.build("PyCall")`
   
7. Open the Julia REPL and install the Julia package `Dojo.jl`: `(type ])`: 
```julia
pkg> add Dojo
```

**Python setup**

8. In your virtual environment, install: `pyjulia`, the interface that lets you call Julia code from Python. 
    - Activate your virtual environement, then run:
    ```bash
    python3 -m pip install julia
    ```

9. In Python run:
```python
import julia
julia.install()
```
to finish the `pyjulia` setup.

We can now call Dojo from Python!

## Documentation
See the [Documentation](https://dojo-sim.github.io/Dojo.jl/dev/) for using Dojo.

## Performance
When Dojo is called from a python script, e.g. `python3 ...` Julia will *just-in-time* compile the solver code which will slow down the overall execution. For larger problems it is advisable to solve a mini problem first to trigger the JIT-compilation and get full performance on the subsequent solve of the actual problem .

## Licence
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Citing
```
@article{howelllecleach2022,
	title={Dojo: A Differentiable Simulator for Robotics},
	author={Taylor, A. Howell and Le Cleac'h, Simon and Kolter, Zico and Schwager, Mac and Manchester, Zachary},
	journal={arXiv preprint arXiv:2203.00806},
	url={https://arxiv.org/abs/2203.00806},
	year={2022}
}
```

## How To Contribute
Please submit a pull request, open an issue, or reach out to: thowell@stanford.edu (Taylor) or simonlc@stanford.edu (Simon)

