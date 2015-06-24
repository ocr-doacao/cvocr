#!/usr/bin/env bash

## To execute do:
# source ./tesseract_install.sh
## or
# chmod +x ./tesseract_install.sh && ./tesseract_install.sh


sudo xargs -a requirements.system apt-get install

pushd .
mkdir ~/tesseract
pushd ~/tesseract

wget https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-3.02.02.tar.gz&can=2&q=
wget https://code.google.com/p/tesseract-ocr/downloads/detail?name=tesseract-ocr-3.02.por.tar.gz&can=2&q=
wget http://www.leptonica.org/source/leptonica-1.72.tar.gz

tar zxf leptonica-1.72.tar.gz
tar zxf tesseract-ocr-3.02.02.tar.gz
tar zxf tesseract-ocr-3.02.por.tar.gz

pushd leptonica-1.72
./configure
make
sudo make install
sudo ldconfig
popd

pushd tesseract-ocr
./autogen.sh
./configure
make
sudo make install
sudo ldconfig
popd

popd


## To install it in $HOME/local:
#
#./autogen.sh
#./configure --prefix=$HOME/local/
#make install
#
## To install it in $HOME/local using Leptonica libraries also installed in $HOME/local:
#
#./autogen.sh
#LIBLEPT_HEADERSDIR=$HOME/local/include ./configure \
#  --prefix=$HOME/local/ --with-extra-libraries=$HOME/local/lib
#make install

