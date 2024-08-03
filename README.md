<p align="center">
    <img width="200" src="https://github.com/Gabrock94/pyaesthetics/blob/master/docs/pyaesthetics_small.png?raw=True" alt="Logo">
</p>

# pyaesthetics
![GitHub release](https://img.shields.io/github/release/Gabrock94/prettywebsite.svg)
[![PyPI](https://img.shields.io/pypi/v/pyaesthetics.svg)](https://badge.fury.io/py/pyaesthetics)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyaesthetics.svg)](https://pypi.python.org/pypi/pyaesthetics/)
[![PyPI status](https://img.shields.io/pypi/status/pyaesthetics.svg)](https://pypi.python.org/pypi/pyaesthetics/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyaesthetics.svg?label=PyPI%20downloads)](https://pypi.python.org/pypi/pyaesthetics/)
[![Downloads](https://static.pepy.tech/badge/pyaesthetics)](https://pepy.tech/project/pyaesthetics)
[![Documentation Status](https://readthedocs.org/projects/prettywebsite/badge/?version=latest)](https://prettywebsite.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/129248933.svg)](https://zenodo.org/badge/latestdoi/129248933)

Pyaesthetics (formlerly known as PrettyWebsite) is a python package designed to estimate visual features concerning the aesthetic appearance of a still image.

## Features
The module can estimate the following features:
-  Brightness (in both the BT709 and BT601 standards)
-  Contrast (RMS or Michelson contrast)
-  Saturation
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

### Tesseract and pytesseract
Tesseract and pytesseract are also required. 
To install tesseract please visit: https://tesseract-ocr.github.io/tessdoc/Installation.html

### Updating the package
To update the package via pip, you can use:
```bash
pip install --user --upgrade pyaesthetics
```

## Example
pyaeshtetics modules can be used one at the time to estimate one specific feature, or they can be automatically called using an automated entrypoint that calls all the available modules at once. 

### Example 1: one single feature (e.g. Brigthness BT601)

```python
#load only the neede functions from the specific module
from pyaesthetics.brightness import relativeluminance_bt601
from pyaeshtetics.utils import sRGB2RGB
import cv2 #to open and handle images

#define the path to a sample image
path_to_img = "/path/to/image/image.jpg"

#load the image
img = cv2.imread(path_to_img)

#convert the image to the RGB colorscheme
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = sRGB2RGB(img)
print(relativeluminance_bt601(img))

```
### Example 2: Complete analysis

```python
import pyaesthetics

#define the path to a sample image
path_to_img = "/path/to/image/image.jpg"

#perform a subset of the analysis using standard parameters
results = pyaesthetics.analysis.analyzeImage(path_to_img, method="fast")
print(results)

```
Or for a faster analysis:

```python
import pyaesthetics

#define the path to a sample image
path_to_img = "/path/to/image/image.jpg"

#perform a subset of the analysis using standard parameters
results = pyaesthetics.analysis.analyzeImage(path_to_img, method="complete")
print(results)
```

## Documentation
You can check the full documentation here: https://prettywebsite.readthedocs.io/en/latest/

## Requirements
- numpy
- scipy
- matplotlib
- pandas
- opencv-python
- imutils
- pytesseract

## Contacts
Feel free to contact me for questions, suggestions or to give me advice as well at: giulio.gabrieli@iit.it or giulio@duck.com

## Scientific Publications that used pyaesthetic
- Gabrieli G. (2018), Using users' physiological response to predict aesthetic experience of websites, Master Degree in Human-Computer Interaction, University of Trento (Italy)
- Gabrieli, G., Bornstein, M. H., Setoh, P., & Esposito, G. (2022). *Machine learning estimation of users’ implicit and explicit aesthetic judgments of web-pages*. Behaviour & Information Technology, 1-11.
- Bizzego, A., Gabrieli, G., Azhari, A., Lim, M., & Esposito, G. (2022). *Dataset of parent-child hyperscanning functional near-infrared spectroscopy recordings*. Scientific Data, 9(1), 625.
- Cianfanelli, B., Esposito, A., Spataro, P., Santirocchi, A., Cestari, V., Rossi-Arnaud, C., & Costanzi, M. (2023). *The binding of negative emotional stimuli with spatial information in working memory: A possible role for the episodic buffer*. Frontiers in Neuroscience, 17, 445.
- Music A., Maerten A., Wagemans J. (2023).*Beautification of images by generative adversarial networks*. Journal of Vision 2023;23(10):14.
- Veldhuizen M. (2024), Analyzing the Role of Aesthetic Features in Packaging Designs  on Consumer Responses: The Case of Specialty Coffee, Master Degree in Communication Science, Vrije Universiteit (Netherlands)

## Presentation
- Gabrieli, G., Scapin, G., & Esposito, G. (2022). Pyaesthetic, a python package for empirical aesthetic analysis. XXVII
Conference of the International Association of Empirical Aesthetics, Philadelphia, United States. https://giuliogabrieli.it/posters/iaea2022/

## Sponsors
The project has been sponsored by Gitkraken. 

## Coffee?
<a href='https://ko-fi.com/B0B3K45F' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://az743702.vo.msecnd.net/cdn/kofi2.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
