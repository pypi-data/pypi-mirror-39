
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def hokuyo_angle_limits(p1, p2):
    line_x = [0.8, 21.21, -0.8, -21.21]
    line_y = [-0.8, -21.21, -0.8, -21.21]
    x1, x2 = line_x[p1], line_x[p2]
    y1, y2 = line_y[p1], line_y[p2]
    plt.plot([x1, x2], [y1, y2], 'b')

def hokuyo_range_limits():
    # copied and modified from:
    # https://github.com/matplotlib/matplotlib/issues/8046/#issuecomment-278312361
    # Ellipse parameters
    D_0 = 2
    D_1 = 60
    x, y = 0, 0
    # Figure setup
    fig, ax = plt.subplots()

    # Inner Arc
    ax.add_patch(Arc((x, y), D_0, D_0,
                     theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))
    # Outer Arc
    ax.add_patch(Arc((x, y), D_1, D_1,
                     theta1=-45, theta2=225, edgecolor='b', linewidth=1.5))

def hokuyo_limits():
    p1_1, p1_2 = 0, 1
    p2_1, p2_2 = 2, 3
    hokuyo_range_limits()
    hokuyo_angle_limits(p1_1, p1_2)
    hokuyo_angle_limits(p2_1, p2_2)
    plt.show()

if __name__ == '__main__':
    plot_stuff = hokuyo_limits()