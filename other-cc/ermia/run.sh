#!/bin/bash

if [ ! -d build ]; then
  mkdir build
  cd build
  cmake ../ -DCMAKE_BUILD_TYPE=Release
  make -j
  cd ..
fi

cd build
/home/ubuntu/sto/mount_hugepages.sh 102400
./run_script.sh
python3 /home/ubuntu/send_email.py -e 'Ermia' e-*-results.txt
sudo shutdown -h +1
