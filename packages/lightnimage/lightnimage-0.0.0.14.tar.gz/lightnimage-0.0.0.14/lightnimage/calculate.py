import numpy as np


def average_2d(array, area=None):
    """
    Given a 2 dimensional array this function will calculate and return the average of all the elements. The additional
    area argument can be used to specifiy a sub range of indices to be used for the average.
    The area parameter has to be a tuple of the form:
    ( (axis0_start_index, axis0_end_index), (axis1_start_index, axis1_end_index) )

    CHANGELOG

    Added 16.11.2018

    @param np.ndarray array:
    @param tuple area:
    @return:
    """
    if isinstance(area, tuple):
        x_sequence, y_sequence = area
    elif area is None:
        x_sequence = (0, array.shape[0] - 1)
        y_sequence = (0, array.shape[1] - 1)
    else:
        raise TypeError("area input of type {} not supported".format(type(area)))

    # Iterating over all the specified elements, calculating the sum, while also counting the elements,
    # so that later on the average can be calculated as the sum divided by the amount
    summation = 0
    amount = 0

    it = np.nditer(array, flags=['multi_index'])
    while not it.finished:
        y_index, x_index = it.multi_index

        if x_sequence[0] <= x_index <= x_sequence[1] and y_sequence[0] <= y_index <= y_sequence[1]:
            summation += it[0]
            amount += 1

        it.iternext()

    return summation / amount


def threshold_sequencing(array, threshold):
    """
    Given an 1 dimensional array and a threshold value, this function will iterate the array and search sub sequences,
    where the value of array element surpasses the threshold. A list with tuples will be returned, where a tuple
    consists of two indices for the array, the first being the index, where the value first exceeded the threshold and
    the second index being where the value dropped beneath the thr again.

    CHANGELOG

    Added 16.11.2018

    @param np.ndarray array:
    @param float threshold:
    @return:
    """
    sequences = []

    sequence_start = None
    it = np.nditer(array, flags=['multi_index'])
    while not it.finished:

        if sequence_start is None:
            # This means no value was bigger than the threshold yet, so no sequence has started
            # We are only searching for a value bigger than the threshold.
            if it[0] >= threshold:
                sequence_start = it.multi_index[0]

        else:
            # This means we are in the middle of a sequence. When we find a single value
            # that is smaller than the threshold, the sequence ends
            if it[0] < threshold:
                # Saving the sequence with the end being the current index
                sequences.append((sequence_start, it.multi_index[0]))
                sequence_start = None

        it.iternext()

    return sequences


def combinations_2d(iterable1, iterable2):
    """
    Given two lists, a list with all possible combinations of elements from the two lists will be returned. The
    combinations will be in the form of tuples, where the first element is always from the list that was given as
    the first argument to this function.

    CHANGELOG

    Added 16.11.2018

    @param list iterable1:
    @param list iterable2:
    @return:
    """
    combinations = []

    for i in iterable1:
        for j in iterable2:
            combinations.append((i, j))

    return combinations
