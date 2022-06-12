FROM ubuntu:20.04

WORKDIR /dojopip

COPY . .

ENV PY_VERSION=3.6.6

# added from https://rtfm.co.ua/en/docker-configure-tzdata-and-timezone-during-build/
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt update -y 

# added to avoid this warning: https://github.com/moby/moby/issues/27988
RUN apt-get install -y dialog apt-utils 
# added to avoid this issue https://github.com/phusion/baseimage-docker/issues/319
RUN apt install -y --no-install-recommends apt-utils


# added libjpeg-dev for pillow, cf https://stackoverflow.com/questions/44043906/the-headers-or-library-files-could-not-be-found-for-jpeg-installing-pillow-on
RUN apt install -y make build-essential libssl-dev libjpeg-dev zlib1g-dev \
 libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev\
 libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
 python-openssl git vim 


# Install pyenv
RUN git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv 

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
RUN echo 'export PATH="/opt/julias/julia-1.7/bin:$PATH"' >> ~/.bashrc
RUN /bin/bash -c "source /root/.bashrc"


ENV PYTHON_CONFIGURE_OPTS="--enable-shared"

RUN $HOME/.pyenv/bin/pyenv install $PY_VERSION


# Set default python and python3 to our newly installed python
RUN unlink /usr/bin/python3
RUN ln -s $HOME/.pyenv/versions/$PY_VERSION/bin/python3 /usr/bin/python3
RUN ln -s $HOME/.pyenv/versions/$PY_VERSION/bin/python3 /usr/bin/python
RUN echo 'export PATH="$HOME/.pyenv/versions/$PY_VERSION/bin:$PATH"' >> ~/.bashrc
RUN /bin/bash -c "source /root/.bashrc"

# Install python libraries
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install matplotlib
RUN python3 -m pip install meshcat
RUN python3 -m pip install gym

# Install julia dependencies
RUN python3 -m pip install julia
RUN python3 -m pip install jill


RUN python3 -c "from jill.install import install_julia; install_julia(confirm=True)"
RUN python3 -c "import julia; julia.install()"


#added var JULIA_SSL_NO_VERIFY_HOSTS to be able to download julia registry https://discourse.julialang.org/t/julia-1-6-corporate-firewall-could-not-download-https-pkg-julialang-org-registries/60665
RUN julia -e 'ENV["JULIA_SSL_NO_VERIFY_HOSTS"] = "julialang.org"; using Pkg; Pkg.add("PyCall"); Pkg.build("PyCall"); try; Pkg.add("Dojo"); catch LoadError; end; try; Pkg.add("Dojo"); catch LoadError; end'











