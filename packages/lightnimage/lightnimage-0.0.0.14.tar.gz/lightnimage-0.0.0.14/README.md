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

### 0.0.0.12 - 05.12.2018

- Minor bug fix in the grouping engine

### 0.0.0.13 - 06.12.2018

- Added documentation for the grouping engine class
- Fixed an error in the grouping engine where the edge case of a single area would return an empty list
- Extended the detection demo notebook

### 0.0.0.14

- Added "SimpleLightningPreprocessingEngine": An engine for usage in preprocessing images before finding the 
areas. Separates the given image into pure black and pure white, by using the mean and max of the image as parameters 
to a callback function (given through the engine config) to calculate a dynamic threshold on which to separate white 
and black
- Added "CustomSequenceAreaSegmentationEngine": Allows to extract areas of Lighting from an image, by extraction 
sequences from the row and column sums of the images axes and then building all possible combinations from those to get 
2D areas. The callback function that calculates the sequences can be passed as engine config.
- Added function "draw_areas" to utils, which will draw the given areas onto a given plot
- Fixed a duplicate bug in the grouping engine