'''
A smoke test for showing map without line features.
'''
import sys
sys.path.append('..')

from staticmap import Line
from tools.static_map_base_layer import StaticMapBaseLayer

m = StaticMapBaseLayer(600, 600, 80)

southwest = [-83.721154, 42.287215]
northeast = [-83.710182, 42.293970]

coordinates = [southwest, northeast]
line_outline = Line(coordinates, 'white', 6)
line = Line(coordinates, '#D2322D', 4)

m.add_line(line_outline)
m.add_line(line)

image = m.render_without_features() # *** THIS METHOD IS NEW ***
image.save('umich_no_features.png')