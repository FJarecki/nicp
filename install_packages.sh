#!/bin/sh
apt-get update  # To get the latest package lists

apt install git -y
apt install cmake -y
apt install libeigen3-dev -y
apt install libsuitesparse-dev -y
apt install qtdeclarative5-dev -y
apt install qt5-qmake -y
apt install libqglviewer-dev-qt5 -y
apt install libflann-dev -y
apt install libopencv-dev -y
apt install freeglut3-dev -y

pip install numpy
pip install scipy
pip install opencv-python
pip install quaternion
pip install glob

pip3 install numpy
pip3 install scipy
pip3 install glob
pip3 install open3d
