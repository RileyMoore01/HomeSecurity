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
  cd raspi3/
  sudo chmod +x install_optimized_opencv.sh
  sudo ./install_optimized_opencv.sh #this script will take a long time to execute.
</pre>
