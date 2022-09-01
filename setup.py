from setuptools import setup
import os

datadir = os.path.join("share","data")
datafiles = [(d,[os.path.join(d,f) for f in files]) for d, folders, files in os.walk(datadir)]

setup(name='pyaesthetics',
    version='0.0.7.6',
    description='Images aesthetic analysis',
    long_description="A python package to estimate aesthetics visual features from still images.",
    url='https://github.com/Gabrock94/pyaesthetics',
    author='Giulio Gabrieli',
    author_email='gack94@gmail.com',
    packages=['pyaesthetics'],      
    install_requires=[
        'numpy',
        'opencv-python',
        'scipy',
        'matplotlib',
        'imutils',
        'pytesseract',
        'pandas'
    ],
    keywords = ["Image","Analysis","Aesthetic",'Visual','Features'],
    classifiers = [ 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False,
    include_package_data=True,
    data_files = datafiles)
