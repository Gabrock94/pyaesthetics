---
title: 'pyaesthetics: A Python package for the estimation of visual features from images'
tags:
  - Python
  - Aesthetics
  - Features extraction
  - Image analysis

authors:
  - name: Giulio Gabrieli
    orcid: 0000-0002-9846-5767
    equal-contrib: false
    affiliation: "1"

affiliations:
 - name: Center for Life Nano- and Neuro-Science, Istituto Italiano di Tecnologia, 00161, Rome, Italy
   index: 1

date: 3 August 2024
bibliography: paper.bib
---

# Summary

The growing amount of research in neuroaesthetics, an interdisciplinary field exploring the neural basis of aesthetic experiences and preferences, particularly concerning the aesthetics of visual stimuli, highlights the interest of researchers in the complex interplay between sensory perception and emotional response. Despite the volume of research, the number of features analyzed by each study is generally limited to a small subset of visual properties. This lack of interest in multiple and more complex features can be partly explained by the absence of tools that allow for the efficient estimation of a wide range of features from images, making the process very time-consuming and leading to significant challenges in result reproducibility, as variations in implementation and feature estimation occur. The pyaesthetics package is designed to streamline and simplify the feature estimation process by providing access to a multitude of functions that can be used to extract the most commonly analyzed visual features.

# Statement of need

`pyaesthetics` is an Python package for the estimation of visual features from still images. The API for `pyaesthetics` was
designed to provide modules for different visual features that are commonly used in studies of empirical aesthetics, and it also provides
a simple entrypoints to conduct automati analysis or users with limited coding knowledge.
Among the features, pyaesthetics allows for the estimation of the brightness, contrast, saturation, visual complexity, symmetry, colorfulness, and color distribution. The updated list of features estimable with `pyaesthetics` is available in the [repository of the project](https://github.com/Gabrock94/pyaesthetics), as well as in the [documentation of the project](https://prettywebsite.readthedocs.io/en/latest/index.html). 
`pyaesthetics` is aimed at researchers in the field of empirical aesthetics, however its modules can be of help also for researchers in the Social Sciences, and especially Psychology, as well as Neuroscience, to explore the visual properties of stimuli employed in different research projects. Moreover, `pyaesthetics` may be employed by visual designers, artists, and other individuals who need to explore the visual properties of images of various nature.

The package has already been used a number of peer-reviewed scientific publications [bizzego2022dataset;gabrieli2023machine;cianfanelli2023binding;music2023beautification;liu2024mothers], as well as master's and Ph.D.'s theses [Gabrieli2018;Gabrieli2021;Veldhuizen2024]. 


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References