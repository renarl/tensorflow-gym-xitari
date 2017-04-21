FROM tensorflow/tensorflow:1.1.0-py3
MAINTAINER Renars Liepins <renarl@gmail.com>


RUN apt-get update && apt-get install -y \
        sudo \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


###############################
# Xitari with a python bridge #
###############################

# instal torch with deps
# https://hub.docker.com/r/mindcont/torch/~/dockerfile/
# Run Torch7 installation scripts
RUN git clone https://github.com/torch/distro.git /root/torch --recursive && cd /root/torch && \
  bash install-deps && \
  ./install.sh

# Export environment variables manually
ENV LUA_PATH='/root/.luarocks/share/lua/5.1/?.lua;/root/.luarocks/share/lua/5.1/?/init.lua;/root/torch/install/share/lua/5.1/?.lua;/root/torch/install/share/lua/5.1/?/init.lua;./?.lua;/root/torch/install/share/luajit-2.1.0-beta1/?.lua;/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua'
ENV LUA_CPATH='/root/.luarocks/lib/lua/5.1/?.so;/root/torch/install/lib/lua/5.1/?.so;./?.so;/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/5.1/loadall.so'
ENV PATH=/root/torch/install/bin:$PATH
ENV LD_LIBRARY_PATH=/root/torch/install/lib:$LD_LIBRARY_PATH
ENV DYLD_LIBRARY_PATH=/root/torch/install/lib:$DYLD_LIBRARY_PATH
ENV LUA_CPATH='/root/torch/install/lib/?.so;'$LUA_CPATH


# install xitari
# from https://github.com/kuz/DeepMind-Atari-Deep-Q-Learner/blob/master/install_dependencies.sh
RUN cd /root/torch && git clone https://github.com/deepmind/xitari.git && cd xitari && \
    luarocks make

# install alewrap
RUN cd /root/torch && git clone https://github.com/deepmind/alewrap.git && cd alewrap && \
    luarocks make

# install lutorpy
# need to import xitari through lua in python
RUN pip --no-cache-dir install \
    lutorpy


##############
# OpenAI Gym #
##############

# install gym dependencies
RUN apt-get update && apt-get install -y \
        git \
        python-numpy \
        python-dev \
        cmake \
        zlib1g-dev \
        libjpeg-dev \
        xvfb \
        libav-tools \
        xorg-dev \
        python-opengl \
        libboost-all-dev \
        libsdl2-dev \
        swig \
        libgtk2.0-dev \
        wget \
        unzip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install gym
RUN pip --no-cache-dir install \
    gym[all]==0.8.1


########
# Misc #
########

# useful python libs
RUN pip --no-cache-dir install \
    scikit-image \
    plotly
