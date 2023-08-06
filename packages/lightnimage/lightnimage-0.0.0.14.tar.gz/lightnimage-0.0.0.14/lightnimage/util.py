import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_areas(ax, areas, color='r'):
    """
    Draws an outlining rectangle for each given area in the list onto the given plot

    CHANGELOG

    Added 09.12.2018

    :param plt.axis ax:     The axis object, which defines the (sub)plot, on which the areas are supposed to be
                            drawn to
    :param list areas:      The list of area tuples, which define the areas to be drawn
    :param string color:    The color of the area edges. DEFAULT is "r" for red
    :return: void
    """
    for area in areas:
        # Calculating the defining features of the area, which are needed to define the rectangular
        # patch
        start_vector = (area[0][0], area[1][0])
        width = area[0][1] - area[0][0]
        height = area[1][1] - area[1][0]

        # Adding the area as a colored rectangle to the plot
        rectangle_patch = patches.Rectangle(start_vector, width, height, linewidth=1, edgecolor=color, facecolor='none')
        ax.add_patch(rectangle_patch)


def next_numerical_file_name(folder_path, base=''):
    """

    CHANGELOG

    Added 19.11.2018

    @param str folder_path:
    @param str base:
    @return:
    """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        # Iterating through all the elements of the folder and looking only at the file names.
        # We try to convert a file name to an integer to find out if it is a numerical file name.
        # We make a list of all the numbers, that are already used and then return the next bigger
        # number, that can still be used.

        already_used_numbers = []
        for root, dirs, files in os.walk(folder_path):

            # only looking at the files:
            for file_name in files:  # type: str
                try:
                    # Getting the pure name of the file, WITHOUT the file type extension.
                    # Also removing the base name string, that is either prefix or suffix
                    file_name_pure = file_name.split('.')[0].replace(base, '')
                    number = int(file_name_pure)
                    already_used_numbers.append(number)
                finally:
                    pass

        # At the end we retrieve the maximum used number and return the numerically next one
        max_already_used_number = max(already_used_numbers)
        return max_already_used_number + 1

    else:
        raise Exception('The given path {} is not a valid folder for file enumeration !'.format(folder_path))
