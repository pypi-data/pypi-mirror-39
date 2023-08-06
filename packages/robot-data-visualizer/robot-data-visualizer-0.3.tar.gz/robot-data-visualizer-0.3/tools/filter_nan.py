def filter_nan(file_name):
    """
    This function filters out NaN values from a csv file.

    :param file_name: Name of csv file to filter.
    :type file_name: str.
    :return: None
    """

    with open(file_name, 'r')as r:
        lines = r.readlines()
    with open(file_name, 'w')as w:
        for l in lines:
            if 'nan' not in l:
                w.write(l)
