'''
This is a smoke test for tools.staticmap_for_gps.
'''
from staticmap import Line
import matplotlib.pyplot as plt
import os
import sys
sys.path.append('..')

from tools.data_manager import DataManager
from tools.static_map_base_layer import StaticMapBaseLayer
from tools.staticmap_for_gps import generate_coordinates

def plot_gps_on_map():
    '''
    This functions is used to plot gps points on map
    :return: (px, py)coordinates of every gps data
    '''
    data_manager = DataManager('2013-01-10')
    # Download and extract sensor data
    data_manager.setup_data_files('sensor_data')
    # load gps
    data_manager.load_gps()

    map = StaticMapBaseLayer(1000, 1000, 80)

    coordinates = generate_coordinates(data_manager.data_dict)
    # Put image in the corresponding data directory
    os.chdir(data_manager.data_dir)

    line = Line(coordinates, 'red', 4)
    map.add_line(line)

    image = map.render_without_features()
    image.save('umich_empty.png')

    points = map.extract_line_points()
    x_coords = [item[0] for item in points]
    y_coords = [item[1] for item in points]

    plt.imshow(image)
    plt.plot(x_coords, y_coords)
    plt.show(block=True)  # block program until window is closed

    return points

if __name__ == '__main__':
    plot_gps_on_map()
