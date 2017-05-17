[![Build Status](https://travis-ci.org/ivanplex/dinosaur.svg?branch=master)](https://travis-ci.org/ivanplex/dinosaur)

# Real-time Synchronous Audio Multicast

## Raspberry Pi Setup

```bash
apt-get update
apt-get install python3-pip
apt-get install portaudio19-dev
pip-3.2 install pyaudio
```
Clone external library (reedsolomon):
```bash
cd dinosaur/external
git clone https://github.com/tomerfiliba/reedsolomon.git
#Molularise Reedsolomon library
touch reedsolomon/__init__.py
```
