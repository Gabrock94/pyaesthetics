from setuptools import setup
import os

datadir = os.path.join("share","data")
datafiles = [(d,[os.path.join(d,f) for f in files]) for d, folders, files in os.walk(datadir)]

setup(name='prettywebsite',
    version='0.0.1',
    description='Website aesthetic analysis in Python',
    long_description="A simple python package for aesthetic analysis of web pages.",
    url='https://github.com/Gabrock94/PrettyWebsite',
    download_url='',
    author='Giulio Gabrieli',
    author_email='gack94@gmail.com',
    license='GPL',
    packages=['prettywebsite'],      
    install_requires=[
        'numpy',
        'opencv-python',
        'scipy',
        'matplotlib'
    ],
    keywords = ["Website","Analysis","Aesthetic"],
    classifiers = [ 
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        
        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved ::  GNU General Public License v3 (GPLv3)',
        
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
    include_package_data=True,
    data_files = datafiles)
