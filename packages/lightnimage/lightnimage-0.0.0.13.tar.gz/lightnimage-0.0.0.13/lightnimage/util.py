import os


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
