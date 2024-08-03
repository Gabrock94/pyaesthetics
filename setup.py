#!/usr/bin/env python

from distutils.core import setup
import os

datadir = os.path.join("share","data")
datafiles = [(d,[os.path.join(d,f) for f in files]) for d, folders, files in os.walk(datadir)]

setup(name='pyaesthetics',
    version='0.0.8.1',
    description='Images aesthetic analysis',
    long_description="A python package to estimate aesthetics visual features from still images."
    long_description_content_type='text/markdown',  # Make sure this matches the format of your README file
    author='Giulio Gabrieli',
    author_email='gack94@gmail.com',
    url='https://github.com/Gabrock94/pyaesthetics',
    packages=['pyaesthetics'],
        install_requires=[
            'numpy',
            'opencv-python',
            'scipy',
            'matplotlib',
            'imutils',
            'pytesseract',
            'pandas'
            'pillow',
            'face-recognition'
        ],
    keywords = ["Image","Analysis","Aesthetic",'Visual','Features'],
    classifiers = [ 
        'Development Status :: 5 - Production/Stable',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',

        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    zip_safe=False,
    include_package_data=True,
    data_files = datafiles)
