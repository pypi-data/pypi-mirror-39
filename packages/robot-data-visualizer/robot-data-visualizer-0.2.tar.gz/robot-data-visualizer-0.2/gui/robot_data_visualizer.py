import os
import sys
sys.path.append('.')
sys.path.append('..')

import warnings
warnings.filterwarnings("ignore")

import time
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.lines as lines
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import tkinter as tk

from tools.get_dates_umich import get_dates_umich
from tools.staticmap_for_gps import map_for_gps
from tools.data_manager import DataManager
from tools.view_lidar import hokuyo_plot
from tools.view_lidar import threshold_lidar_pts


class VisualizerFrame(tk.Frame):
    """
    This is the main window where the robot data is seen by the user.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label = None
        self.ax_map = None
        self.ax_gps = None
        self.ax_lidar = None
        self.map_plot = None
        self.gps_plot = None
        self.lidar_plot = None
        self.canvas = None
        self.data_manager = None
        self.gps_data = None
        self.lidar_data = None
        self.gps_on = False
        self.map_on = False
        self.lidar_on = False
        self.map_image = None
        self.widgets()

    def widgets(self):
        """
        Set up widgets for the frame.

        :return: None
        """
        self.label = tk.Label(self, text="Viewer")
        self.label.pack(side=tk.TOP)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax_map = self.fig.add_subplot(111)
        self.ax_gps = self.fig.add_subplot(111)
        self.ax_lidar = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def callback_initialize_data_manager(self):
        """
        This callback responds to the *Load Data* button.

        :return: None
        """
        date = self.parent.toolbar.date.get()
        if self.data_manager is None:
            self.setup_data(date)
        else:
            if self.data_manager.date is not date:
                os.chdir('../..') # TODO patched here - add this to end of load_gps() / load_lidar() functions
                self.setup_data(date)
            else:
                pass

    def setup_data(self, date):
        """
        This function sets up all of the data (except lidar) needed by the application.

        :param date: Determines which date from the robotics dataset to use.
        :type date: str.
        :return: None
        """
        if self.data_manager is not None:
            os.chdir(self.data_manager.owd)
            self.ax_gps.clear()
            self.ax_map.clear()
            self.ax_lidar.clear()
            self.canvas.draw()
            self.gps_on = False
            self.map_on = False
            self.lidar_on = False
        self.parent.set_status('DM_START', hold=True)
        self.data_manager = DataManager(date)
        self.data_manager.setup_data_files('sensor_data')
        self.data_manager.load_gps()
        x_coords, y_coords = map_for_gps(self.data_manager.data_dict, self.data_manager.data_dir)
        self.lidar_data = None
        self.gps_data = [x_coords, y_coords] # in image coords
        self.map_image = mpimg.imread(os.path.join(self.data_manager.data_dir, 'map.png'))
        self.label.config(text='Viewer')
        self.parent.set_status('DM_READY')

    def callback_gps_on(self):
        """
        This callback responds to the *On* button under the *GPS Control* menu.

        :return: None
        """
        if not self.lidar_on:
            if not self.gps_on:
                self.gps_on = True
                self.parent.set_status('GPS_START')
                idx = self.get_idx_for_gps_update()
                self.update_timestamp(idx)
                self.gps_plot = self.ax_gps.plot(self.gps_data[0][:idx], self.gps_data[1][:idx], 'r')[0]
                self.canvas.show()
                self.parent.set_status('GPS_READY')
            else:
                pass
        else:
            self.callback_lidar_off()
            self.callback_gps_on()

    def callback_gps_off(self):
        """
        This callback responds to the *Off* button under the *GPS Control* menu.

        :return: None
        """
        if self.gps_on:
            self.gps_on = False
            self.update_gps(0)
            self.label.config(text='Viewer')
            self.parent.set_status('GPS_REMOVE')
        else:
            pass

    def callback_gps_slider_changed(self, event):
        """
        This callback responds to the *Off* button under the *GPS Control* menu.
        :return: None
        """
        self.gps_on = True
        idx = self.get_idx_for_gps_update()
        self.update_gps(idx)
        self.update_timestamp(idx)
        self.parent.set_status('GPS_UPDATE')

    def update_gps(self, idx):
        """
        This function updates the GPS data that is displayed in the main viewing window.
        :param idx: Index into the array of GPS data that is to be displayed.
        :type idx: int.
        :return: None
        """
        if self.gps_data is not None:
            self.gps_plot.set_xdata(self.gps_data[0][:idx])
            self.gps_plot.set_ydata(self.gps_data[1][:idx])
            self.canvas.draw()
        else:
            pass

    def update_timestamp(self, idx):
        """
        This function updates the timestamp in the main viewing window.

        :param idx: Index into the array of GPS data to be used for retrieval of the time stamp.
        :type idx: int.
        :return: None
        """
        curr_tstamp = self.get_timestamp_for_gps_update(idx)
        self.label.config(text=str('time stamp: ' + curr_tstamp))

    def get_idx_for_gps_update(self):
        """
        This function returns the index to be used for updating the GPS data.
        :return: int -- the index to be used for the GPS update
        """
        slider_val = self.parent.control.gps_control.selection_scale.get()
        idx_ratio = len(self.gps_data[0]) / 100
        return int(slider_val * idx_ratio)

    def get_timestamp_for_gps_update(self, gps_data_idx):
        """
        This function returns the timestamp in a readable format for the given GPS data index.

        :param gps_data_idx: Index into the array of GPS data to be used for retrieval of the time stamp.
        :return: str -- the timestamp
        """
        idx_ratio = len(self.data_manager.data_dict['gps']['tstamp']) / len(self.gps_data[0])
        idx = int(gps_data_idx * idx_ratio) - 1
        ts = int(self.data_manager.data_dict['gps']['tstamp'][idx] / 1000000)
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def callback_map_on(self):
        """
        This callback responds to the *On* button under the *Map Control* menu.

        :return: None
        """
        if not self.lidar_on:
            if not self.map_on:
                self.map_on = True
                if self.map_image is not None:
                    self.ax_map.imshow(self.map_image)
                    # draw scale on the map
                    map_scale = self.get_map_scale()
                    line = lines.Line2D([0, 200], [0, 0], linewidth=4, color='b')
                    self.ax_map.add_line(line)
                    distance = map_scale * 200
                    if distance > 1000:
                        scale_str = "scale = " + str(float("%.2f" % (distance / 1000))) + " kilometers"
                    else:
                        scale_str = "scale = " + str(float("%.2f" % (distance))) + " meters"
                    self.ax_map.text(0, -10, scale_str, fontsize=8)
                    self.canvas.draw()
                    self.parent.set_status('MAP_READY')
                else:
                    self.parent.set_status('MAP_ERROR')
            else:
                pass
        else:
            self.callback_lidar_off()
            self.callback_map_on()

    def callback_map_off(self):
        """
        This callback responds to the *Off* button under the *Map Control* menu.

        :return: None
        """
        if self.map_on:
            self.map_on = False
            self.ax_map.clear()
            if self.gps_on:
                self.gps_on = False
                self.callback_gps_on() # because the previous line clears both map and gps
            self.canvas.draw()
        else:
            pass

    def callback_date_changed(self):
        """
        This callback responds to a change in the date selection menu in the toolbar.

        :return: None
        """
        new_date = self.parent.toolbar.date.get() # Need to call get() because this is a StringVar object
        if self.parent.toolbar.date is not new_date:
            self.parent.toolbar.date.set(new_date)
        else:
            pass

    def get_map_scale(self):
        """
        This function calculates the map scale in units of meters per pixel.

        :return: float64 -- map scale (m/px)
        """
        k = 111000 # meters per degree of latitude (approx.)
        lat_range = self.data_manager.data_dict['gps_range'][0]
        d_lat_range = abs(lat_range[0] - lat_range[1])
        d_x_pixels = abs(max(self.gps_data[0]) - min(self.gps_data[0]))
        map_scale = d_lat_range * k / d_x_pixels
        return map_scale # units of meters per pixel

    def callback_lidar_slider_changed(self, event):
        self.lidar_on = True
        idx = self.get_idx_for_lidar_update()
        self.update_lidar(idx)
        # self.update_timestamp(idx)
        self.parent.set_status('Lidar updated')

    def get_idx_for_lidar_update(self):
        """
        This function returns the index to be used for updating the Lidar data.

        :return: int -- the index to be used for the Lidar update
        """
        slider_val = self.parent.control.lidar_control.selection_scale.get()
        idx_ratio = len(self.lidar_data) / 100
        return max(int(slider_val * idx_ratio) - 1, 0)

    def update_lidar(self, idx):
        if self.lidar_data is not None:
            xt, yt, _ = threshold_lidar_pts(self.lidar_data[idx])
            self.lidar_plot.set_xdata(xt)
            self.lidar_plot.set_ydata(yt)
            self.canvas.draw()
        else:
            pass

    def callback_lidar_on(self):
        # Turn off gps and map because the lidar cannot be overlaid at this time.
        if not self.lidar_on:
            self.lidar_on = True
            self.callback_map_off()
            self.callback_gps_off()
            if self.data_manager is None:
                self.callback_initialize_data_manager()
            if not 'lidar' in self.data_manager.data_dict.keys():
                self.data_manager.setup_data_files('hokuyo')
                pickled = True
                delete_pickle = False
                self.data_manager.load_lidar(4000, pickled, delete_pickle) # TODO - global constant for lidar samples
                self.lidar_data = self.data_manager.data_dict['lidar']

            xlimits, ylimits = [-32, 32], [-32, 32]
            self.ax_lidar.set_xlim(xlimits)
            self.ax_lidar.set_ylim(ylimits)
            hokuyo_plot(self.ax_lidar)
            xt, yt, _ = threshold_lidar_pts(self.lidar_data[0])
            self.lidar_plot = self.ax_lidar.plot(xt, yt, 'r.')[0]
            self.canvas.show()
        else:
            pass


    def callback_lidar_off(self):
        if self.lidar_on:
            self.lidar_on = False
            self.ax_lidar.clear()
            self.canvas.draw()
        else:
            pass


class ToolbarFrame(tk.Frame):
    """
    This class represents the toolbar at the top of the window.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.date = None
        self.dates = get_dates_umich()
        self.load_button = None
        self.option_menu = None
        self.widgets()

    def widgets(self):
        """
        Set up widgets for the frame.

        :return: None
        """
        self.dates = get_dates_umich()
        self.load_button = tk.Button(self, text="Load Data")
        self.load_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.date = tk.StringVar(self)
        self.date.set(self.dates[24])
        self.option_menu = tk.OptionMenu(self, self.date, *self.dates, command=self.callback_date_changed)
        self.option_menu.pack(side=tk.LEFT, padx=2, pady=2)

    def bind_widgets(self):
        """
        Bind widgets to their callback functions.

        :return: None
        """
        self.load_button.config(command=self.parent.window.callback_initialize_data_manager)

    def callback_date_changed(self, event):
        self.parent.window.callback_date_changed()

class ControlFrame(tk.Frame):
    """
    This class represents the controls on the right hand side of the main
    window. There are two nested classes for the slam and map controls.
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=400)
        self.parent = parent
        self.root = parent
        self.slam_control = None
        self.map_control = None
        self.lidar_control = None
        self.widgets()

    class GpsControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.selection_scale = None
            self.scale_val = None
            self.on_button = None
            self.off_button = None
            self.widgets()

        def widgets(self):
            """
            Set up widgets for the frame.

            :return: None
            """
            label = tk.Label(self, text="GPS Control", bg="blue", fg="white")
            label.pack(side=tk.TOP, fill=tk.X)

            self.selection_scale = tk.Scale(self, orient=tk.HORIZONTAL, to=100, variable=self.scale_val)
            self.selection_scale.set(100)
            self.selection_scale.pack(side=tk.TOP)

            self.on_button = tk.Button(self, text="On", bg="green", fg="white")
            self.on_button.pack(side=tk.LEFT)

            self.off_button = tk.Button(self, text="Off", bg="red", fg="white")
            self.off_button.pack(side=tk.RIGHT)

        def bind_widgets(self):
            """
            Bind widgets to their callback functions.

            :return: None
            """
            self.on_button.config(command=self.root.window.callback_gps_on)
            self.off_button.config(command=self.root.window.callback_gps_off)
            self.selection_scale.bind("<ButtonRelease-1>", self.root.window.callback_gps_slider_changed)


    class MapControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.on_button = None
            self.off_button = None
            self.widgets()

        def widgets(self):
            """
            Set up widgets for the frame.

            :return: None
            """
            label = tk.Label(self, text="Map Control", bg="blue", fg="white")
            label.pack(fill=tk.X)

            self.on_button = tk.Button(self, text="On", bg="green", fg="white")
            self.on_button.pack(side=tk.LEFT)

            self.off_button = tk.Button(self, text="Off", bg="red", fg="white")
            self.off_button.pack(side=tk.RIGHT)

        def bind_widgets(self):
            """
            Bind widgets to their callback functions.

            :return: None
            """
            self.on_button.config(command=self.root.window.callback_map_on)
            self.off_button.config(command=self.root.window.callback_map_off)

    class LidarControlFrame(tk.Frame):

        def __init__(self, parent, root):
            tk.Frame.__init__(self, parent, width=400)
            self.parent = parent
            self.root = root
            self.scale_val = None
            self.on_button = None
            self.off_button = None
            self.widgets()

        def widgets(self):
            """
            Set up widgets for the frame.

            :return: None
            """
            label = tk.Label(self, text="Lidar Control", bg="blue", fg="white")
            label.pack(side=tk.TOP, fill=tk.X)

            self.selection_scale = tk.Scale(self, orient=tk.HORIZONTAL, to=100, variable=self.scale_val)
            self.selection_scale.set(100)
            self.selection_scale.pack(side=tk.TOP)

            self.on_button = tk.Button(self, text="On", bg="green", fg="white")
            self.on_button.pack(side=tk.LEFT)

            self.off_button = tk.Button(self, text="Off", bg="red", fg="white")
            self.off_button.pack(side=tk.RIGHT)

        def bind_widgets(self):
            """
            Bind widgets to their callback functions.

            :return: None
            """
            self.on_button.config(command=self.root.window.callback_lidar_on)
            self.off_button.config(command=self.root.window.callback_lidar_off)
            self.selection_scale.bind("<ButtonRelease-1>", self.root.window.callback_lidar_slider_changed)

    def widgets(self):
        """
        Set up widgets for the frame.

        :return: None
        """
        self.gps_control = self.GpsControlFrame(self, self.root)
        self.gps_control.pack(fill=tk.X)
        self.map_control = self.MapControlFrame(self, self.root)
        self.map_control.pack(fill=tk.X)
        self.lidar_control = self.LidarControlFrame(self, self.root)
        self.lidar_control.pack(fill=tk.X)

    def bind_widgets(self):
        """
        Bind widgets to their callback functions.

        :return: None
        """
        self.gps_control.bind_widgets()
        self.map_control.bind_widgets()
        self.lidar_control.bind_widgets()


class MainWindow(tk.Tk):
    """
    This is the main window for the application. Here the main layout is
    established using a combination of the above classes and individual
    tkinter widgets.
    """

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.status_text = dict(READY="Ready",
                                DM_START="Initializing data manager ...",
                                DM_READY="Data is ready",
                                DM_NOT_READY="Data not loaded",
                                GPS_START="GPS loading ...",
                                GPS_READY="GPS is ready",
                                GPS_REMOVE="GPS removed",
                                GPS_UPDATE="GPS updated",
                                MAP_START="Map loading ...",
                                MAP_READY="Map is ready",
                                MAP_REMOVE="Map removed",
                                MAP_ERROR="Must load data before map can be displayed")
        self.STATUS_DELAY = 2000 # (ms) delay between status changes
        self.title("Robot Data Visualizer")
        self.mainWidgets()


    def mainWidgets(self):
        """
        Set up widgets for the main window frame.

        :return: None
        """
        # Toolbar
        self.toolbar = ToolbarFrame(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Status bar
        self.status = tk.Label(self, text=self.status_text['READY'], bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Controls - GPS and Map
        self.control = ControlFrame(self)
        self.control.pack(side=tk.RIGHT, fill=tk.Y)

        # Main viewing window
        self.window = VisualizerFrame(self)
        self.window.pack(side=tk.LEFT, padx=2, pady=2)

        # Bind widgets to their callback functions
        self.toolbar.bind_widgets()
        self.control.bind_widgets()


    def set_status(self, status, hold=False):
        """
        This function sets the status bar at the bottom of the window (with a time delay).

        :param status: Key to look up status message in the status_text dictionary.
        :type status: str.
        :param hold: When *hold=True*, the status update will not time out.
        :type hold: bool.
        :return: None
        """
        if status in self.status_text.keys():
            self.status.config(text=self.status_text[status])
            if not hold:
                self.status.after(self.STATUS_DELAY, lambda: self.status.config(text=self.status_text['READY']))
        else:
            self.status.config(text=str(status))
            if not hold:
                self.status.after(self.STATUS_DELAY, lambda: self.status.config(text=self.status_text['READY']))

if __name__ == '__main__':
    app = MainWindow(None)
    app.mainloop()
