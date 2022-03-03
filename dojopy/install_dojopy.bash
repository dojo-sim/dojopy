echo "█████ STEP 0/X -define arguments"
# directory where we cloned the dojopy package
WORKING_DIR=${1:-$HOME/Documents/dojopip}
# directory where python environment will be installed
ENV_DIR=${2:-$WORKING_DIR/auto_generated_dojo_env}
# directory of the cloned dojopy package
DOJOPY_DIR=${3:-$WORKING_DIR/dojopy}
# directory where pyenv will be installed
PYENV_DIR=${4:-$HOME/.pyenv}
# version of python that we will install
PY_VERSION=${5:-3.8.2}
# custom python path
PY_PATH=${PYENV_DIR}/versions/${PY_VERSION}/bin/python3

echo "STEP 0: starting dojopy installation"
echo "WORKING_DIR" $WORKING_DIR
echo "ENV_DIR" $ENV_DIR
echo "DOJOPY_DIR" $DOJOPY_DIR
echo "PY_VERSION" $PY_VERSION
echo "PYENV_DIR" $PYENV_DIR
echo "PY_PATH" $PY_PATH

# This tutorial was performed as the root user on Ubuntu 18.04.

echo "█████ STEP 1/X - pyenv installation"
echo "█████ stage 1 - update and install dependencies"
apt update -y


echo "█████ stage 2 - install all of pyenv’s dependencies"
apt install -y make build-essential libssl-dev zlib1g-dev \
> libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
> libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl\
> git


echo "█████ stage 3 - clone the repository"
echo "█████ /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\need to delete this line"
# rm -rf $PYENV_DIR
git clone https://github.com/pyenv/pyenv.git $PYENV_DIR


echo "█████ stage 4 - configure the environment"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
source ~/.bashrc # not sure this is needed


echo "█████ stage 5 - verify the installation - display list of available python versions"
$PYENV_DIR/bin/pyenv install --list

echo "█████ STEP 2/X - build a custom python binary with pyenv"
echo "█████ stage 1 - we use pyenv to build a custom python binary in ${PYENV_DIR}"
echo "█████ Do not be surprised if it takes a while for this command to run. Pyenv is building this version of Python from source."
# PYTHON_CONFIGURE_OPTS="--enable-shared" $PYENV_DIR/bin/pyenv install $PY_VERSION


echo "█████ stage 2 - verify the installation - display the list of python versions installed through pyenv, you should see $PY_VERSION displayed"
$PYENV_DIR/bin/pyenv versions



echo "█████ STEP 3/X - create a virtual environment linked to previouly created custom python binary"
echo "█████ stage 1 - create a virtual environment"
$PY_PATH -m pip install virtualenv
echo "█████ /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\need to delete this line"
rm -rf $ENV_DIR
$PY_PATH -m venv $ENV_DIR
source ${ENV_DIR}/bin/activate


echo "█████ STEP 4/X - add dependencies to the newly created virtual environment located at $ENV_DIR"
$ENV_DIR/bin/python3 -m pip install julia
$ENV_DIR/bin/python3 -m pip install jill
echo "█████ STEP 5/X - install julia at /opt/julias/"
$ENV_DIR/bin/python3 ${DOJOPY_DIR}/setup_julia.py
echo "█████ STEP 6/X - install pyjulia in the virtual environment: $ENV_DIR"
$ENV_DIR/bin/python3 ${DOJOPY_DIR}/setup_pyjulia.py

# Install Dojopy dependencies
echo "█████ STEP 7/X - Install Dojopy dependencies in the virtual environment: $ENV_DIR"
$ENV_DIR/bin/python3 -m pip install matplotlib
$ENV_DIR/bin/python3 -m pip install meshcat
$ENV_DIR/bin/python3 -m pip install gym

deactivate
