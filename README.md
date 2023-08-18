# HomeSecurity
Making an at-home security system

<h1>Hardware</h1>
-Raspberry Pi 3<br/>
-Raspberry Pi Camera Module<br/>
-Custom Detection Software<br/>

<h1>Command line</h1>
<pre>
  sudo apt-get update
  sudo apt-get install python-picamera python3-picamera
  sudo apt-get install python3-pip
  sudo pip3 install "picamera[array]"
  sudo apt-get install python3-opencv
  sudo apt install -y gpac
  pip3 install tensorflow
</pre>
For best results, compile opencv natively with ARM optimizations
<pre>
  #!/bin/bash
  
  sudo apt-get purge wolfram-engine
  sudo apt-get purge libreoffice*
  sudo apt-get clean
  sudo apt-get autoremove
  
  sudo apt-get update && sudo apt-get upgrade
  sudo apt-get install -y build-essential cmake pkg-config
  sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
  sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
  sudo apt-get install -y libxvidcore-dev libx264-dev
  sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
  sudo apt-get install -y libcanberra-gtk*
  sudo apt-get install -y libatlas-base-dev gfortran
  sudo apt-get install -y python2.7-dev python3-dev
  
  cd ~
  wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
  unzip opencv.zip
  wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
  unzip opencv_contrib.zip
  
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  sudo python3 get-pip.py
  
  pip install numpy
  
  cd ~/opencv-3.3.0/
  mkdir build
  cd build
  cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..
  
  sudo su
  echo "Expanding swapfile to 2048 MB"
  echo "CONF_MAXSWAP=2048" >> /etc/dphys-swapfile
  sudo /etc/init.d/dphys-swapfile stop
  sudo /etc/init.d/dphys-swapfile start
  exit
  
  make -j4
  
  sudo make install
  sudo ldconfig
  
  sudo su
  echo "Resizing swapfile back to 100 MB"
  echo "CONF_MAXSWAP=100" >> /etc/dphys-swapfile
  sudo /etc/init.d/dphys-swapfile stop
  sudo /etc/init.d/dphys-swapfile start
  exit
</pre>
<pre>
  cd raspi3/
  sudo chmod +x install_optimized_opencv.sh
  sudo ./install_optimized_opencv.sh #this script will take a long time to execute.
</pre>

<h3>Credit</h3>
<a href='pyimagesearch'>pyimagesearch</a>
