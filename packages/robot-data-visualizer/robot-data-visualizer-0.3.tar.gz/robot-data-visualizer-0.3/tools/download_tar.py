"""
This script downloads a tar file from the UMich robotics dataset

code referenced from: http://blog.ppkt.eu/2014/06/python-urllib-and-tarfile/
"""


import os
import urllib.request
os.chdir('..')
owd = os.getcwd() # original working directory
data_dir = None


def ensure_data_dir_exists():
    """
    This function makes sure that there is a *data* directory in which to put the downloaded files.

    :return: None
    """
    global owd, data_dir
    p = owd
    p = os.path.join(p, 'data')
    if not os.path.exists(p):
        os.mkdir(p)
    data_dir = p


def download_tar(base_name, date, data_type):
    """
    This function downloads the tar file and puts it in the *data* directory.

    :param base_name: Base url
    :type base_name: str.
    :param date: Date to select in the data set.
    :type date: str.
    :param data_type: Selects the type of data to download (lidar or GPS).
    :type data_type: str.
    :return: str. -- name of file that was downloaded
    """
    ensure_data_dir_exists()
    global data_dir
    os.chdir(data_dir)
    if data_type is 'sensor_data': # miscellaneous sensors, incl. GPS
        tmp = '%s/sensor_data/' % base_name
        fname = '%s_sen.tar.gz' % date
    elif data_type is 'hokuyo': # hokuyo lidar scanner
        tmp = '%s/hokuyo_data/' % base_name
        fname = '%s_hokuyo.tar.gz' % date
    # TODO throw exception for invalid data_type
    url = tmp + fname
    path = os.path.join(data_dir, fname)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    else:
        pass
    return fname
