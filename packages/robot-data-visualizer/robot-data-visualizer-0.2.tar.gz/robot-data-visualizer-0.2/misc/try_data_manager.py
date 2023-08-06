# Test an import of the DataManager class

import sys
sys.path.append('..')

import traceback
from tools.data_manager import DataManager


def main():
    try:
        # Initialize with desired date from the UMich dataset
        dm = DataManager('2013-01-10')
        # Download and extract sensor data
        dm.setup_data_files('sensor_data')
        # Download and extract data for the hokuyo lidar scanner
        dm.setup_data_files('hokuyo')
        # load gps
        dm.load_gps()
        # load first 100 scans of lidar
        dm.load_lidar(100)
        print('Successful load of data')
    except Exception as ex:
        print(ex)
        traceback.print_exc()

if __name__ == '__main__':
    main()