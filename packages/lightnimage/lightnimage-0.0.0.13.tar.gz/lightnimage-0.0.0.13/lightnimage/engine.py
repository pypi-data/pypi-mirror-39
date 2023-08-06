# 16.11.2018
# Standard library
# Python 2 compatibility for the print function syntax
from __future__ import print_function
import math
from collections import defaultdict

# third party
import numpy as np
from pprint import pprint

# local package
from lightnimage.image import LightningImage
from lightnimage.calculate import *


# ABSTRACT BASE CLASSES #


class AbstractVectorisationEngine:
    """

    CHANGELOG

    Added 05.11.2018

    """

    def __init__(self, lightning_image):
        """

        CHANGELOG

        Added 05.11.2018

        @param LightningImage lightning_image:
        """
        self.lightning_image = lightning_image
        self.array = self.lightning_image.array

    def __call__(self, *args, **kwargs):
        """

        CHANGELOG

        Added 05.11.2018

        @param args:
        @param kwargs:
        @return:
        """
        raise NotImplementedError()


class AbstractAreaSegmentationEngine:

    def __init__(self, config):
        pass

    def __call__(self, lightning_image):
        """
        The engine gets called on a single lightning image object and returns a list of dicts, each containing a value
        for a x, y, length and width keys, defining a rectangle, where the procedure guesses a lightning can be found

        CHANGELOG

        Added 13.11.2018

        @param lightning_image:
        @return:
        """
        raise NotImplementedError()


# IMPLEMENTATIONS #

class SimpleAreaSegmentationEngine(AbstractAreaSegmentationEngine):
    """
    This procedure assumes the image is already processed.

    Given an Image object, this algorithm will calculate the pixel sums along the rows and the columns of the picture.
    The resulting intensity function is then segmented into sub sequences along the axis's by watching, when the
    function first exceeds a certain threshold and when it drops below it again.
    From these sequences along the axis all possible combinations(=areas on the picture) are computed. These areas are
    suspected to contain intensity maximums. In the last step the average of each area is checked against another
    threshold to remove false positives from the final result.

    CHANGELOG

    Added 16.11.2018
    """
    DEFAULT_CONFIG = {
        'threshold':        1.0,
        'checking':         True,
        'check_threshold':  0.03,
    }

    def __init__(self, config):
        """
        The constructor.

        The config dict can have the following parameters:
        - threshold:        A float, which defines the factor between a value of the axis sum function and the global
                            average of the latter that qualifies a value as surpassing the threshold.
                            A threshold RELATIVE to the average of the function. DEFAULT is 1.0
        - checking:         boolean flag of whether or not to perform the last checking operation
        - check_threshold:  A float threshold value relative to 255 the average of an area has to have to qualify as a
                            valid solution to the problem. DEFAULT is 0.03, equates to roughly a grayscale value of 7,
                            which has to be the average of an area.

        CHANGELOG

        Added 16.11.2018

        @param dict config:
        """
        AbstractAreaSegmentationEngine.__init__(self, config)
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(config)

        self.current = None

    def __call__(self, lightning_image):
        """
        The main function executed, when the engine is called.

        CHANGELOG

        Added 16.11.2018

        @param LightningImage lightning_image:
        @return: List(Tuple())
        """
        # A copy of the image object is being made, so transformations can be used without disturbing the original
        # image
        self.current = LightningImage(lightning_image)

        # Calculating the row and column sums of the grayscale values
        self.x_sums = self.current.row_sum()
        self.y_sums = self.current.column_sum()

        # Calculating the mean value of both these functions
        x_average = np.average(self.x_sums)
        y_average = np.average(self.y_sums)

        # Calculating the thresholds based on the factor given by the config
        self.x_threshold = x_average * self.config['threshold']
        self.y_threshold = y_average * self.config['threshold']

        # Getting all the possible areas
        x_sequences = threshold_sequencing(self.x_sums, self.config['threshold'])
        y_sequences = threshold_sequencing(self.y_sums, self.config['threshold'])

        areas = combinations_2d(x_sequences, y_sequences)

        if self.config['checking']:
            # Creating areas only from all the possible combinations of two axis's sub sequences also creates a lot
            # of false areas.
            # Here we go through all the areas and essentially compute the average amount of signal within them. Areas
            # are only part of the final solution, if the average within them surpasses a certain threshold
            result = []
            for area in areas:
                # Calculating the average within these areas and only using these that contain a high enough value
                av = average_2d(self.current.array, area)
                # print("Checking {} with average {}".format(str(area), av))
                if (av / 255) >= self.config['check_threshold']:
                    result.append(area)
            return result

        return areas


class SimpleAreaGroupingEngine:
    """
    The problem:
    When processing the lightnings with the SimpleAreaSegmentationEngine, it can happen, that at one point the
    the lightning is more dim in brightness and thus it gets detected as two separate lightnings. But in some cases it
    would be better to have it detected as a whole.

    This is what this engine does. Bases on a weight function and a threshold, it computes for each pair of areas on
    the whole picture, whether it is reasonable to believe, that they belong to a single lightning or not.

    CHANGELOG

    Added 05.12.2018
    """

    """
    CHANGELOG
    
    Added 05.12.2018
    
    Changed 06.12.2018
    Changed the default formula for computation to from "d * s" to "d + math.sqrt(s)"
    """
    DEFAULT_CONFIG = {
        'weight_function': lambda d, s: d + math.sqrt(s),
        'threshold':       10**4
    }

    def __init__(self, config):
        """
        The constructor

        The config dict can have the following parameters:
        - weight_function:  This is a callable object, which will expect two parameters, the first one being the
                            the distance between two areas and the second one being their combined size (added up).
                            The function has to return a value which will then be compared to the given threshold
        - threshold:        The value which will be compared with the result of the weight function, that has been
                            computed from the pair of two areas.
                            Is the weight smalled than the threshold, the two areas are grouped, otherwise not
        CHANGELOG

        Added 05.12.2018

        :param config:
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config.update(config)

    def __call__(self, areas):
        """
        Given a list of areas, this engine will return another list of areas, with the same amount or less areas, where
        some of the original areas have been grouped together by the rules of the engine configuration. These grouped
        areas are the combined into one bigger area, which spans over all the original areas.

        CHANGELOG

        Added 05.12.2018

        :param areas: A list of all the areas of a lightning detection
        :return: List()
        """
        # First we need to decide which areas will be put in a group with each other. This we will do, by computing
        # Whether to group for each pair:
        groups = self.group_areas(areas)
        combined_areas = []
        for group in groups:
            combined_area = self.combine_areas(group)
            combined_areas.append(combined_area)

        return combined_areas

    def group_areas(self, areas):
        """
        Given a list of areas, this function computes which areas belong to one group, following the rules given by
        the weight function and the threshold of the engine configuration. A list of lists will be returned, where each
        sub list contains all the areas belonging to one group

        CHANGELOG

        Added 05.12.2018

        :param areas:
        :return: List(List(Tuple(Tuple(int, int), Tuple(int, int))))
        """
        group_membership = defaultdict(list)

        # 06.12.2018
        # This is an edge case I haven't previously thought about: When there is only one area the loop down
        # blow does not even get executed properly, which leads to an empty list being returned
        if len(areas) == 1:
            return [areas]

        for i in range(len(areas)):

            for j in range(i + 1, len(areas)):
                area_i = areas[i]
                area_j = areas[j]

                # Calculating the distance and the size and using that as parameters to the weight function
                distance = self.area_distance(area_i, area_j)
                size = self.area_size(area_j) + self.area_size(area_j)
                weight = self.config['weight_function'](distance, size)

                if weight < self.config['threshold']:
                    group = group_membership[area_j] + group_membership[area_i] + [area_i, area_j]
                    # removing duplicates from that list
                    group = list(set(group))
                    group_membership[area_j] = group
                    group_membership[area_i] = group

                else:
                    group_membership[area_i].append(area_i)
                    group_membership[area_j].append(area_j)

        groups = []
        for group in list(group_membership.values()):
            if group not in groups:
                groups.append(group)

        return groups

    @staticmethod
    def combine_areas(areas):
        """
        Given a list of areas, this function will compute a new area, which will include all the given areas.

        CHANGELOG

        Added 05.12.2018

        :param areas:   A list of all the areas to be combined into one big area
        :return: area
        """
        x_min = math.inf
        x_max = 0
        y_min = math.inf
        y_max = 0

        for area in areas:
            x_start = area[0][0]
            y_start = area[1][0]

            x_end = x_start + (area[0][1] - area[0][0])
            y_end = y_start + (area[1][1] - area[1][0])

            if x_start < x_min:
                x_min = x_start
            if y_start < y_min:
                y_min = y_start
            if x_end > x_max:
                x_max = x_end
            if y_end > y_max:
                y_max = y_end

        return (x_min, x_max), (y_min, y_max)

    @staticmethod
    def area_size(area):
        """
        Returns the size of the area, by multiplying width and height.

        CHANGELOG

        Added 05.12.2018

        :param Tuple(Tuple(int,int)) area:  THe tuple describing the two dimensional are in a x y plane
        :return:  int
        """
        width = area[0][1] - area[0][0]
        height = area[1][1] - area[1][0]
        return width * height

    @staticmethod
    def area_distance(area1, area2):
        """
        Calculates the distance between two given areas (Obviously they have to be in the same coordinate system).
        The distance is calculated between the centers of the areas!
        Returns the float distance value

        CHANGELOG

        Added 05.12.2018

        :param area1:
        :param area2:
        :return: float
        """
        # First we need the center point of each area
        area1_center = SimpleAreaGroupingEngine.area_center(area1)
        area2_center = SimpleAreaGroupingEngine.area_center(area2)

        # Calculating the distance between two 2 dimensional points
        distance = math.sqrt((area1_center[0] - area2_center[0])**2 + (area1_center[1] - area2_center[1])**2)
        return distance

    @staticmethod
    def area_center(area):
        """
        Calculates the center point of a given area tuple. The center will be returned as a tuple of two FLOAT
        values, the first element being the x coordinate and the second the y coordinate.

        CHANGELOG

        Added 05.12.2018

        :param Tuple(Tuple(int,int)) area:  THe tuple describing the two dimensional are in a x y plane
        :return: Tuple(int, int)
        """
        center = (area[0][0] + (area[0][1] - area[0][0]) / 2, area[1][0] + (area[1][1] - area[1][0]) / 2)
        return center
