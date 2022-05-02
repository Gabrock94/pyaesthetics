<p align="center">
    <img width="200" src="https://github.com/Gabrock94/pyaesthetics/blob/master/docs/pyaesthetics_small.png" alt="Logo">
</p>

# pyaesthetic
![GitHub release](https://img.shields.io/github/release/Gabrock94/prettywebsite.svg)
[![PyPI](https://img.shields.io/pypi/v/pyaesthetics.svg)](https://badge.fury.io/py/pyaesthetics)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyaesthetics.svg)](https://pypi.python.org/pypi/pyaesthetics/)
[![PyPI status](https://img.shields.io/pypi/status/pyaesthetics.svg)](https://pypi.python.org/pypi/pyaesthetics/)
[![Documentation Status](https://readthedocs.org/projects/pyaesthetics/badge/?version=latest)](http://pyaesthetics.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/129248933.svg)](https://zenodo.org/badge/latestdoi/129248933)

Pyaesthetics (formlerly known as PrettyWebsite) is a python package designed to estimate visual features concerning the aesthetic appearance of a still image.

## Features
The module can estimate the following features:
-  Brightness (in both the BT709 and BT601 standards)
-  Visual Complexity (either by using the weight of the image or by Quadratic Tree Decomposition)
-  Simmetry (using Quadratic Tree Decomposition)
-  Colorfulness (in both the HSV and RGB color spaces)
-  Presence and number of human faces
-  Color distribution
-  Number of images within the image
-  Surface of visual and textual areas within the image
-  Ratio between visual and textual areas

## Installation
pyaesthetics can be installed using pip:
```bash
pip install pyaesthetics
```
or manually by downloading or cloning the repository and, from the root folder of the project, running:
```bash
python setup.py pyaesthetics
```

## Example
pyaeshtetics modules can be used one at the time to estimate one specific feature, or they can be automatically called using an automated entrypoint that calls all the available modules at once. 

### Example 1: one single feature (e.g. Brigthness BT601)

```python
#load only the neede functions from the specific module
from pyaesthetics.brightness import relativeLuminance_BT601, sRGB2RGB
import cv2 #to open and handle images

img = "/path/to/image/image.jpg" #path to a sample image

img = cv2.imread(img) #load the image
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert to the RGB colorscheme
img = sRGB2RGB(img) #convert pixels to their linear RGB values
print(relativeLuminance_BT601(img)) #evaluate luminance on the BT601 standard
```
### Example 2: Complete analysis

```python
import pyaesthetics
img = "/path/to/image/image.jpg" #path to a sample image
results = pyaesthetics.analyzeImage(img) #perform all the availabe analysis using standard parameters
print(results)
```

## Documentation
You can check the full documentation here: https://pyaesthetics.rtfd.io (not available yet)

### Requirements
- Numpy
- Scipy
- Matplotlib

## Contacts
Feel free to contact me for questions, suggestions or to give me advice as well at: giulio001@e.ntu.edu.sg or giulio@duck.com

## Coffee?
<a href='https://ko-fi.com/B0B3K45F' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi2.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
