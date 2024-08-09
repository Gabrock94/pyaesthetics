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
- Brightness (in both the BT709 and BT601 standards)
- Contrast (RMS or Michelson contrast)
- Saturation
- Visual Complexity (either by using the weight of the image, by Quadratic Tree Decomposition, or by gradients)
- Simmetry (using Quadratic Tree Decomposition)
- Colorfulness (in both the HSV and RGB color spaces)
- Presence and number of human faces
- Color distribution (16 or 140 W3C colors, or no named colors)
- Number of images within the image
- Surface of visual and textual areas within the image
- Ratio between visual and textual areas
- Ratio between straight and curved lines
- Anisotropy
- Self-similarity (using either the ground, parent, or neighbors method)

## Installation
pyaesthetics can be installed using pip:
```bash
pip install pyaesthetics
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
results = pyaesthetics.analysis.analyze_image(path_to_img, method="fast")
print(results)

```
Or for a faster analysis:

```python
import pyaesthetics

#define the path to a sample image
path_to_img = "/path/to/image/image.jpg"

#perform a subset of the analysis using standard parameters
results = pyaesthetics.analysis.analyze_image(path_to_img, method="complete")
print(results)
```

## Documentation
The updated documentation of pyaesthetics, its modules, as well as a getting started guide and a list of examples can be found on [Read the Docs](https://prettywebsite.readthedocs.io/en/latest/). The documentation of each release version of CLIMADA can be accessed separately through the drop-down menu at the bottom of the left sidebar. 

## Requirements
In order to work correctly, pyaesthetics requires the installation of the following packages.

- numpy
- scipy
- matplotlib
- pandas
- opencv-python
- imutils
- pytesseract
- pillow
- face-recognition
- scikit-image

## Contacts
For questions, suggestions, or advices, you can reach out at: giulio.gabrieli@iit.it or giulio@duck.com

## Scientific Publications that used pyaesthetic
Pyaesthetics has been used in different scientific publication. The most relevant works are listed below.

### Peer-reviewed articles
- Gabrieli, G., Bornstein, M. H., Setoh, P., & Esposito, G. (2022). *Machine learning estimation of users’ implicit and explicit aesthetic judgments of web-pages*. Behaviour & Information Technology, 1-11.
- Bizzego, A., Gabrieli, G., Azhari, A., Lim, M., & Esposito, G. (2022). *Dataset of parent-child hyperscanning functional near-infrared spectroscopy recordings*. Scientific Data, 9(1), 625.
- Cianfanelli, B., Esposito, A., Spataro, P., Santirocchi, A., Cestari, V., Rossi-Arnaud, C., & Costanzi, M. (2023). *The binding of negative emotional stimuli with spatial information in working memory: A possible role for the episodic buffer*. Frontiers in Neuroscience, 17, 445.
- Music A., Maerten A., Wagemans J. (2023).*Beautification of images by generative adversarial networks*. Journal of Vision 2023;23(10):14.
- Liu, Q., Zhu, S., Zhou, X., Liu, F., Becker, B., Kendrick, K. M., & Zhao, W. (2024). Mothers and fathers show different neural synchrony with their children during shared experiences. NeuroImage, 288, 120529.

### Theses
- Gabrieli G. (2018), Using users' physiological response to predict aesthetic experience of websites, Master Degree in Human-Computer Interaction, University of Trento (Italy)
- Veldhuizen M. (2024), Analyzing the Role of Aesthetic Features in Packaging Designs  on Consumer Responses: The Case of Specialty Coffee, Master Degree in Communication Science, Vrije Universiteit (Netherlands)

### Presentation
- Gabrieli, G., Scapin, G., & Esposito, G. (2022). Pyaesthetic, a python package for empirical aesthetic analysis. XXVII
Conference of the International Association of Empirical Aesthetics, Philadelphia, United States. https://giuliogabrieli.it/posters/iaea2022/

## Contribution Guidelines for pyaesthetics

We welcome contributions to the pyaesthetics project! Whether you want to help with code, documentation, or examples, your input is valuable. Here’s how you can contribute:

### How to Contribute

1. **Fork the Repository:**
   - Click the "Fork" button on the top right corner of the repository page to create your own copy of the project.

2. **Clone the Repository:**
   - Clone your fork to your local machine:
     ```bash
     git clone https://github.com/your-username/pyaesthetics.git
     cd pyaesthetics
     ```

3. **Create a Branch:**
   - Create a new branch for your changes:
     ```bash
     git checkout -b your-branch-name
     ```

### Types of Contributions

1. **Code Contributions:**
   - **Bug Fixes:** Help us fix bugs and improve the stability of the project.
   - **New Features:** Implement new features or enhance existing ones.
   - **Performance Improvements:** Optimize code for better performance and efficiency.

2. **Documentation:**
   - Improve existing documentation or add new sections to help users understand and use the project more effectively.

3. **Examples:**
   - Create and share examples to demonstrate how to use various features of the pyaesthetics package.

### Submitting Your Contribution

1. **Commit Your Changes:**
   - Make sure your commits are clear and concise. Follow good commit message practices.
     ```bash
     git add .
     git commit -m "Description of your changes"
     ```

2. **Push to Your Fork:**
   - Push your changes to your forked repository:
     ```bash
     git push origin your-branch-name
     ```

3. **Create a Pull Request:**
   - Go to the original repository and click on the "New Pull Request" button.
   - Select your fork and branch as the source, and the original repository and branch as the target.
   - Provide a clear and descriptive title and description for your pull request.

### Code Review Process

1. **Review:**
   - Your pull request will be reviewed by the maintainers. They may request changes or ask for additional information.
   
2. **Update:**
   - Make any requested changes and update your pull request.

3. **Merge:**
   - Once your pull request is approved, it will be merged into the main branch.

### Additional Notes

- Please ensure that your code follows the project's coding style and conventions. Functions should contain docstrings and follow, if possible PEP8 guidelines. 
- Write tests or samples debug methods for any new features or bug fixes to ensure they work as expected.
- Be respectful and considerate in your communications and contributions.

## Sponsorship
The project has received a one-shot sponsorship for open-source projects by Gitkraken. 
