# Arguments
# version of python that we will install
PY_VERSION=${1:-3.8.2}
# directory where pyenv will be installed
PYENV_DIR=${2:-$HOME/.pyenv}
# directory where python environment will be installed
ENV_DIR=${2:-$HOME/Documents/dojopip/scripts/dojoenv}

PY_DIR=${PYENV_DIR}/versions/${PY_VERSION}/bin/python3

# # This tutorial was performed as the root user on Ubuntu 18.04.
#
# # Step #1: Update and Install Dependencies
# # It’s always a good idea to start off any installation process by updating system packages:
# apt update -y
#
# # Once that has finished up, run the following command to install all of pyenv’s dependencies:
# apt install -y make build-essential libssl-dev zlib1g-dev \
# > libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
# > libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
# > git
#
#
# # Step #2: Clone the Repository
# #To install the latest version of pyenv and provide a straightforward method for updating it, run the following command to pull it down from GitHub:
# rm -rf $PYENV_DIR
# git clone https://github.com/pyenv/pyenv.git $PYENV_DIR
#
#
# # Step #3: Configure the Environment
# # Next, to properly configure pyenv for use on the system, run the following block of commands to set some important environment variables and setup pyenv autocompletion:
# echo 'export PYENV_ROOT="$HOME/Documents/dojopip/scripts/.pyenv"' >> ~/.bashrc
# echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
# source ~/.bashrc # not sure this is needed
#
#
# # Step #4: Verify the Installation
# # To verify that pyenv is installed correctly, we will try installing a new version of Python. First, we will list the available versions of Python:
# $PYENV_DIR/bin/pyenv install --list
#
# # # The list of the available version is long. Let’s go ahead and install Python version 3.8.3:
# # $PYENV_DIR/bin/pyenv install $PY_VERSION
# # Do not be surprised if it takes a while for this command to run. Pyenv is building this version of Python from source.
#
# # Step #5: Use pyenv to build your own Python In PYENV_DIR run:
# PYTHON_CONFIGURE_OPTS="--enable-shared" $PYENV_DIR/bin/pyenv install $PY_VERSION
# # to create a custom binary.
#
# # To verify that Python PY_VERSION is now installed run the pyenv versions command:
# $PYENV_DIR/bin/pyenv versions


# Step #6: (Optional) Create a virtual environment linked to custom_python
# In your shell run:
# $PY_DIR -m pip install virtualenv
# rm -rf $ENV_DIR
# $PY_DIR -m venv $ENV_DIR
source ${ENV_DIR}/bin/activate
#
# # Step #7: Install the Julia programming language (v1.5+ recommended) [Julia Download page]
# $ENV_DIR/bin/python3 -m pip install julia
# $ENV_DIR/bin/python3 -m pip install jill
# $ENV_DIR/bin/python3 setup_julia.py
# $ENV_DIR/bin/python3 setup_pyjulia.py

# # Install Dojopy dependencies
# $ENV_DIR/bin/python3 -m pip install matplotlib
# $ENV_DIR/bin/python3 -m pip install meshcat
# $ENV_DIR/bin/python3 -m pip install gym

# $ENV_DIR/bin/python3 dojopy/demo.py

deactivate
