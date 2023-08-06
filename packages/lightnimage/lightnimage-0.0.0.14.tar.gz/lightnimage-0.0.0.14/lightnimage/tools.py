import matplotlib.pyplot as plt
import matplotlib.patches as patches


from lightnimage.image import LightningImage
from lightnimage.engine import *

import os


def plot_lightning_detection_overview(image, ref_image):
    """
    CHANGELOG

    Added 16.11.2018

    @deprecated

    @param LightningImage image:
    @param LightningImage ref_image:
    @return:
    """
    # Creating the sub plots
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')

    # Calculating a simple subtraction of the two images
    print('Calculating the difference of the pictures')
    subtraction = ref_image - image

    # Plotting that into the first sub plot
    ax1.imshow(subtraction.array, cmap='gray')
    ax1.set_title('difference of the images')

    # Calculating the difference of the two images
    difference = ref_image.difference(image, threshold=70, replace=0)

    # Refining the difference picture to gain a pure mask of the lightning
    print('Processing the difference to get the lightning mask')
    difference.lighten(30, replace=255)

    # Plotting the mask into a subplot
    ax2.imshow(difference.array, cmap='gray')
    ax2.set_title('lightning mask')

    # Computing the areas in which the lightnings are
    print('Calculating the areas, that contain lightning')
    config = {

    }
    area_engine = SimpleAreaSegmentationEngine(config)
    areas = area_engine(difference)

    # Plotting the original picture into the third plot and the calculated areas as red boxed around the lightnings
    ax3.imshow(image.array, cmap='gray')
    ax3.set_title('lightning detection')

    print('Overlaying the detected areas with the original picture')
    for area in areas:
        start = (area[0][0], area[1][0])
        width = area[0][1] - area[0][0]
        height = area[1][1] - area[1][0]
        rect = patches.Rectangle(start, width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax3.add_patch(rect)

    # Removing the lightning from the difference picture by using the mask
    print('Removing the lightning from the difference picture using the lightning mask')
    removed = subtraction.copy()
    removed.transform_masked(lambda v, i, j: 0, difference.get_mask())

    ax4.imshow(removed.array, cmap='gray')
    ax4.set_title('without lightning')

    plt.show()


def plot_simple_lightning_detection(image, ref_image, save_path=None, file_name=None, is_showing=True):
    """
    This function will plot the original pictures and the areas, where the lightnings were detected as
    an overlay of red boxes. Besides the red boxes will be the label, of what the program guesses the
    lightning type to be:
    - "ground": Cloud to ground
    - "cross": Cloud to cloud
    - "???": Couldnt make a guess

    The function will return a list of tuples, where the first element is the string containing the
    type of the lightning and the second being the area tuple describing the area, where the lightning
    can be found.

    CHANGELOG

    Added 19.11.2018

    Changed 19.11.2018
    Fixed bug, where the plot image couldnt be saved

    @param LightningImage image:
    @param LightningImage ref_image:
    @param str save_path:
    @param str file_name:
    @param bool is_showing:
    @return: List(Tuple(str, Tuple(Tuple(int, int), Tuple(int, int))))
    """
    # Creating the sub plots
    f, ax = plt.subplots(1, 1, sharex='col', sharey='row')

    # Calculating a simple subtraction of the two images
    print('Calculating the difference of the pictures')

    # Calculating the difference of the two images
    difference = ref_image.difference(image, threshold=70, replace=0)

    # Refining the difference picture to gain a pure mask of the lightning
    print('Processing the difference to get the lightning mask')
    difference.lighten(30, replace=255)

    # Computing the areas in which the lightnings are
    print('Calculating the areas, that contain lightning')
    config = {

    }
    area_engine = SimpleAreaSegmentationEngine(config)
    areas = area_engine(difference)

    # Filtering out the area that occurs due to the timestamp in the lower right corner
    areas = filter(lambda x: x[0][0] <= image.width * 0.9 or x[1][0] <= image.height * 0.9, areas)

    ax.imshow(image.array, cmap='gray')

    # For each area making a guess if it is a cross or ground lightning
    # depending on whether the area is rather vertical or horizontal
    print('Overlaying the detected areas with the original picture')
    area_types = []
    for area in areas:
        print('Found area {}'.format(str(area)))
        start = (area[0][0], area[1][0])
        width = area[0][1] - area[0][0]
        height = area[1][1] - area[1][0]
        rect = patches.Rectangle(start, width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        # Making the guess
        if width >= 1.3 * height:
            guess = 'cross'
        elif height >= 1.3 * width:
            guess = 'ground'
        else:
            guess = '???'

        # Adding the guessed type and the area, which was guessed for to the list
        # which will be returned at the end
        area_types.append((guess, area))

        # plotting the text
        ax.text(start[0], start[1] - 14, guess, size=7, color='r')

    if save_path is not None:

        # In case a file name is given it will be used
        if file_name is not None:
            # 19.11.2018
            # Changed the image type to SVG and changed the method for creating the path from simple
            # string manipulation to path.join function
            file_name_extended = "{}.svg".format(file_name)
            file_path = os.path.join(save_path, file_name_extended)
            print('Saving as "{}"'.format(file_path))
            plt.savefig(file_path, dpi=600)

    # 19.11.2018
    # Added a flag as parameter, whith which the actual display of the plot can be toggled
    if is_showing:
        plt.show()