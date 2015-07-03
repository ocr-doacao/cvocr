#!/usr/bin/env bash

## To execute do:
# source ./tesseract_install.sh
## or
# chmod +x ./tesseract_install.sh && ./tesseract_install.sh

sudo apt-get update
sudo apt-get install -y python python-pip  python-dev
sudo apt-get install -y tesseract-ocr tesseract-ocr-por
sudo apt-get install -y libatlas-base-dev liblapack-dev git subversion python-virtualenv
sudo pip install numpy scipy
sudo apt-get remove -f ffmpeg x264 libx264-dev
sudo apt-get -qy install libopencv-dev build-essential checkinstall cmake pkg-config yasm libtiff4-dev libjpeg-dev \
 libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine-dev libgstreamer0.10-dev \
 libgstreamer-plugins-base0.10-dev libv4l-dev python-dev python-numpy libtbb-dev libqt4-dev libgtk2.0-dev libfaac-dev \
 libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils \
 ffmpeg

version="$(wget -q -O - http://sourceforge.net/projects/opencvlibrary/files/opencv-unix | egrep -m1 -o '\"[0-9](\.[0-9])+' | cut -c2-)"
sudo mkdir -p /tmp/OpenCV
pushd /tmp/OpenCV
sudo wget -O opencv.zip http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/"$version"/opencv-"$version".zip
sudo unzip opencv.zip
pushd opencv-"$version"
sudo mkdir -p build
pushd build
sudo cmake -D CMAKE_BUILD_TYPE=RELEASE -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON \
 -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..
sudo make -j2
sudo make install
sudo ldconfig

popd
popd
popd
sudo pip install -r requirements.txt
sudo cp ocr.traineddata /usr/share/tesseract-ocr/tessdata/