#!/bin/sh

cd nicp
text=$(pwd)
mkdir build
cd build
cmake ..
make

cd ~

cat >> .bashrc << EOF
# NICP
export NICP_ROOT=$text
export LD_LIBRARY_PATH=\${LD_LIBRARY_PATH}:\${NICP_ROOT}/lib
EOF

source ~/.bashrc

cd $text
cd ..
cd nicp_depth_camera_tracking_code
mkdir build
cd build
cmake ..
make
