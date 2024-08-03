Getting started
=================

pyaeshtetics modules can be used one at the time to estimate one specific feature, or they can be automatically called using an automated entrypoint that calls all the available modules at once.
Here a list of examples of both methods are provided.

Analysis of single feature
############################

If you'd like to estimate a single feature, you can use the specific pair of module/function.
Below, an example of the estimation of the brightness of an image, using the BT601 method.

First load the modules you need.

>>> #load only the neede functions from the specific module
>>> from pyaesthetics.brightness import relativeLuminance_BT601
>>> from pyaeshtetics.utils import sRGB2RGB
>>> import cv2 

Then load the image using cv2.

>>> img = "/path/to/image/image.jpg" #path to a sample image
>>> img = cv2.imread(img) #load the image
>>> img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert to the RGB colorscheme

We then convert the pixels to linear RGB values.

>>> img = sRGB2RGB(img) 

 Finally, extract the luminance. 

>>> print(relativeLuminance_BT601(img)) 

Analysis using the entrypoint module
######################################

Pyaesthetics comes with an *analysis* module, which is an entrypoint to perform two types of analysis ("fast" and "comeplete"), with limited coding.

The "fast" method performs the following analysis: 

* brightness (BT709)
* Visual Complexity (using quadtree decomposition)
* Symmetry (using quadtree decomposition)
* Colorfulness (in the RGB color scheme)
* contrast (Root Mean Square (RMS) method)
* saturation
* ratio between straight and curved lines

The "complete" method performs the following analysis:

* brightness (BT709 and BT601)
* Visual Complexity (using quadtree decomposition)
* Visual Complexity (using the weight method)
* Symmetry (using quadtree decomposition)
* Colorfulness (in HSV and RGB color schemes)
* Face detection and number of faces
* Color detection
* Number of images within an image
* Text to image ratio
* Surface area occupied by text and images
* contrast (Root Mean Square (RMS) and Michelson methods)
* saturation
* ratio between straight and curved lines

To run a fast analysis, use the following snippet of code:

>>> import pyaesthetics
>>> img = "/path/to/image/image.jpg" #path to a sample image
>>> results = pyaesthetics.analysis.analyzeImage(img, method="fast") #perform a subset of the analysis using standard parameters.
>>> print(results)

While to run a complete analysis, you can use the following snippet:

>>> import pyaesthetics
>>> img = "/path/to/image/image.jpg" #path to a sample image
>>> results = pyaesthetics.analysis.analyzeImage(img, method="complete") #perform a subset of the analysis using standard parameters.
>>> print(results)
