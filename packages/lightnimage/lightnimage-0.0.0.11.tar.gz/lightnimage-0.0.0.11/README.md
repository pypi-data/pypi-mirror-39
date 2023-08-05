# Lightnimage

## Installation

pip install lightnimage

## Changelog

### 0.0.0.7 - 06.11.2018

initial version

### 0.0.0.8 - 16.11.2018

- Wrote functions to calculate (in calculate.py):
    - the 2d average of a matrix
    - all combinations of elements from two lists
    - Sequences passing a certain threshold
- Added an engine, which calculates the areas of maximum signal

### 0.0.0.9 - 19.11.2018

- LightningImage class:
    - Added methods, that transform the matrix as a whole, element wise or element 
    wise with an additional mask, dictating where to apply the function
    - Added a copy method
    - Added a method, which will return a boolean (0 and 1 int) mask array based 
    on the image and a threshold value
- tools
    - Added a tool which will plot the basic image detection. Drawing red boxes 
    around the areas where a lightning was found and a label, which contains the guess 
    whether it was a cloud to ground or a cloud to cloud lightning
    
### 0.0.0.10 - 19.11.2018

- tools
    - Fixed bug with saving the figure as file
    
### 0.0.0.11 - 05.12.2018

- Added a jupyter notebook, which illustrates the detection process
- Added the grouping engine, which will group some detected areas together
