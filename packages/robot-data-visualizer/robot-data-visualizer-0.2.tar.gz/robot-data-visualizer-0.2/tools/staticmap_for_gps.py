'''This file is used to generate all points needed for plot in real-time.'''

import os
from staticmap import Line
from tools.static_map_base_layer import StaticMapBaseLayer
from tools.data_manager import DataManager

def generate_coordinates(data_dict):
    '''
    This function preprocess gps data to make it useful for future use.
    :param data_dict: input gps data from dataManager
    :return: coordinates[[lng, lat], [], ...]
    '''
    gps_data = data_dict['gps']
    gps_lat = gps_data['lat']
    gps_lng = gps_data['lng']

    coordinates = []

    # for i in range(0, len(gps_lat), 50):
    for i in range(0, len(gps_lat)):
        coordinates.append([gps_lng[i], gps_lat[i]])

    return coordinates

def divide_coordinates(coordinates):
    '''
    Divide coordinates into about 50 pieces for following use.
    :param coordinates: coordinates contains gps data.
    :return: divided coordinates
    '''
    interval = len(coordinates) // 50 + 1
    divided_coordinates = []
    for i in range(0, len(coordinates), interval):
        divided_coordinates.append(coordinates[i: i + interval])
    return divided_coordinates

def map_for_gps_gif():
    '''
    This function is used to generate 48 pictures to generate gif.
    '''
    dm = DataManager('2013-01-10')
    # Download and extract sensor data
    dm.setup_data_files('sensor_data')
    # load gps
    dm.load_gps()

    m = StaticMapBaseLayer(1000, 1000, 80)

    coordinates = generate_coordinates(dm.data_dict)
    # Put image in the corresponding data directory
    os.chdir(dm.data_dir)

    line = Line(coordinates, 'red', 4)
    m.add_line(line)

    divided_coordinates = divide_coordinates(coordinates)
    length = len(divided_coordinates)
    for i in range(length):
        temp_line = Line(divided_coordinates[i], 'red', 4)
        m.add_line(temp_line)
        print('Total : ' + str(length)  + '  So far :' + str(i))
        if i != 0:
            prev_line = Line([divided_coordinates[i - 1][-1], divided_coordinates[i][0]], 'red', 4)
            m.add_line(prev_line)
        image = m.render()
        image.save('umich' + str(i) + '.png')


def map_for_gps(data_dict, data_dir):
    '''
    This function is used to generate essential (px_x, px_y) coordinates to draw path.
    :param data_dict: where to get data
    :param data_dir: where to put output picture
    :return: x_coordinates and y_coordinates in pixels for gps data
    '''
    m = StaticMapBaseLayer(1000, 1000, 80)

    coordinates = generate_coordinates(data_dict)
    # Put image in the corresponding data directory
    os.chdir(data_dir)

    line = Line(coordinates, 'red', 4)
    m.add_line(line)

    image = m.render_without_features()
    image.save('map.png')

    points = m.extract_line_points()
    x_coords = [item[0] for item in points]
    y_coords = [item[1] for item in points]

    return x_coords, y_coords
