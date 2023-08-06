''' Modification to the original staticmaps API, which can be found at
    https://github.com/komoot/staticmap/blob/master/staticmap/staticmap.py'''

from math import sqrt, log, tan, pi, cos
from staticmap import StaticMap
from PIL import Image


RECT = 90
HALF_DEGREE = 180
FULL_DEGREE = 360


class StaticMapBaseLayer(StaticMap):
    '''
    This is a overide class inherited from StaticMap. We overide some functions there to
    get something we want.
    '''

    def __init__(self, width, height, padding):
        super().__init__(width, height, padding) # call constructor for inherited class

    def _lon_to_x(self, lon, zoom):
        """
        transform longitude to tile number
        :type lon: float
        :type zoom: int
        :rtype: float
        """
        if not (-HALF_DEGREE <= lon <= HALF_DEGREE):
            lon = (lon + HALF_DEGREE) % FULL_DEGREE - HALF_DEGREE

        return ((lon + HALF_DEGREE) / FULL_DEGREE) * pow(2, zoom)


    def _lat_to_y(self, lat, zoom):
        """
        transform latitude to tile number
        :type lat: float
        :type zoom: int
        :rtype: float
        """
        if not (-RECT <= lat <= RECT):
            lat = (lat + RECT) % HALF_DEGREE - RECT

        return (1 - log(tan(lat * pi / HALF_DEGREE) + 1 / cos(lat * pi / HALF_DEGREE)) / pi) \
               / 2 * pow(2, zoom)


    def _simplify(self, points, tolerance=11):
        """
        :param points: list of lon-lat pairs
        :type points: list
        :param tolerance: tolerance in pixel
        :type tolerance: float
        :return: list of lon-lat pairs
        :rtype: list
        """
        if not points:
            return points

        new_coords = [points[0]]

        for point in points[1:-1]:
            last = new_coords[-1]

            dist = sqrt(pow(last[0] - point[0], 2) + pow(last[1] - point[1], 2))
            if dist > tolerance:
                new_coords.append(point)

        new_coords.append(points[-1])

        return new_coords



    def extract_line_points(self):
        '''
        This method is not in the original API
        This function extract line features.
        :return: points((px, py),(),...)
        '''
        for line in self.lines:
            points = [(
                self._x_to_px(self._lon_to_x(coord[0], self.zoom)),
                self._y_to_px(self._lat_to_y(coord[1], self.zoom)),
            ) for coord in line.coords]

            if line.simplify:
                points = self._simplify(points)
        return points


    def render_without_features(self, zoom=None, center=None):
        """
        render static map with all map features that were added to map before
        :param zoom: optional zoom level, will be optimized automatically if not given.
        :type zoom: int
        :param center: optional center of map, will be set automatically from markers if not given.
        :type center: list
        :return: PIL image instance
        :rtype: Image.Image
        """

        if not self.lines and not self.markers and not self.polygons and not (center and zoom):
            raise RuntimeError("cannot render empty map, add lines / markers / polygons first")

        if zoom is None:
            self.zoom = self._calculate_zoom()
        else:
            self.zoom = zoom

        if center:
            self.x_center = self._lon_to_x(center[0], self.zoom)
            self.y_center = self._lat_to_y(center[1], self.zoom)
        else:
            # get extent of all lines
            extent = self.determine_extent(zoom=self.zoom)

            # calculate center point of map
            lon_center, lat_center = (extent[0] + extent[2]) / 2, (extent[1] + extent[3]) / 2
            self.x_center = self._lon_to_x(lon_center, self.zoom)
            self.y_center = self._lat_to_y(lat_center, self.zoom)

        image = Image.new('RGB', (self.width, self.height), self.background_color)

        self._draw_base_layer(image)
        # This is what draws the features in the original class - which we don't want
        # self._draw_features(image)

        return image
