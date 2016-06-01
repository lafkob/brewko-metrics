#!/bin/bash

# Download Chadwick, build, and install
#wget https://github.com/chadwickbureau/chadwick/archive/v0.6.5.tar.gz
tar xzvf v0.6.5.tar.gz
cd chadwick-0.6.5
autoreconf -i
./configure
make
sudo make install
