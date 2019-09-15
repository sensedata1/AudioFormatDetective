#!/bin/bash -x

apt-get update
apt-get install -y apt-utils
wget https://downloads.sourceforge.net/project/audiotools/audiotools/3.1.1/audiotools-3.1.1.tar.gz
tar -xvzf audiotools-3.1.1.tar.gz

cd audiotools-3.1.1

apt-get -y install libcdio-utils
apt-get -y install python-pyaudio python3-pyaudio
apt-get -y install vim
apt-get -y install make
apt-get -y install cron
apt-get -y install python-setuptools

make install

cd ..

pip install --upgrade setuptools
pip install -r requirements.txt
pip install SpeechRecognition
pip install pydub
pip install watchdog
pip install pyinstaller


pyinstaller --onefile AudioFormatDetectiveSTSR.py
