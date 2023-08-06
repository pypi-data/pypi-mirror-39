[![Build Status](https://travis-ci.org/klatimer/robot-data-visualizer.svg?branch=dev)](https://travis-ci.org/klatimer/robot-data-visualizer)

# Robot Data Visualizer
Welcome to our GitHub repository!

This is our package's [PyPI website](https://pypi.org/project/robot-data-visualizer/).

This project was started with the intention of providing an easy tool for
visualizing robotics data. Currently, only the University of Michigan's
NCLT data set is used, which can be found here: http://robots.engin.umich.edu/nclt/

* PRETTY PICTURE HERE (get people excited to run this thing)

## Structure
    robot-data-visualizer/
      |- README.md
      |- gui
         |- robot_data_visualizer.py
      |- test
         |- run_test.py
         |- test_data_loader.py
         |- test_data_manager.py
         |- ...
      |- misc
         |- iterative_closest_point.py
         |- static_map_example.py
         |- try_data_manager.py
         |- ...
      |- tools/
         |- __init__.py
         |- data_loader.py
         |- data_manager.py
         |- download_tar.py
         |- filter_nan.py
         |- get_dates_umich.py
         |- read_hokuyo_30m.py
         |- static_map_base_layer.py
         |- staticmap_for_gps.py
         |- tar_extract.py
      |- docs/
         |- Component Specification.pdf
         |- Functional Specification.pdf
         |- Makefile
         |- make.bat
         |- build/
            |- ...
         |- index.rst
         |- misc.rst
         |- ...
      |- setup.py
      |- .gitignore
      |- .travis.yml
      |- LICENSE
      |- requirements.txt
      |- environment.yml

## Getting Started

### Installing from PyPI
You can type following to install directly.
```bash
> pip install robot-data-visualizer
```

### Installing from source

The official distribution is on GitHub, and you can clone the repository using:
```bash
> git clone https://github.com/klatimer/robot-data-visualizer
```
Then you need to go to the project's root directory by typing `cd robot-data-visualizer`.

### Setup dependencies
To install all the dependencies, you have two options.

Option 1: Use pip to install all dependencies.
```bash
> pip install -r requirements.txt
```

Option 2: Use virtual environment 
```bash
> source activate environment.yml
```

To install the package, you can type:
```bash
> python setup.py install
```

### Tests
We are using Travis CI for continuous intergration testing. You can check out the current status 
[here](https://travis-ci.org/klatimer/robot-data-visualizer).

## Overview

This project focus on building a tool to make it more convenient for 
Robotic researcher to visualize their complex robot data, 
without wasting to much time in process data and see how it goes.

In general, the data is composed by two kinds of data: GPS data and LIDAR data.


### To visualize GPS data:


First type `cd gui` at root directory of this project to go to gui directory, then type
```bash
> python robot_data_visualizer
```

Then you can see a graphic user interface here:
* @ken Put A newest GUI here without any operation.

To use this GUI, you can follow the instructions here:
* Choose date of data then press `Load Data` button at top-left.
* Wait for all data has been loaded successfully.
* Press `On` or `Off` button of GPS Control to show gps path or not. Also you can drag the slider to see gps path in different completion.
* Press `On` or `Off` button of Map Control to show the overlay map or not.

Then you can see a pretty GUI shows here:
* @ken, put a complete photo of GUI here.


### To visualize LIDAR data:
* @ken Optional if LIDAR can be integrated greatly.


## Documentation
To generate the project's documentation, open up a terminal from the project root
directory and type `cd doc`

Then, to generate the documentation type:
`make html` and open the `index.html` file in `_build/html`.

## License
This project utilizes the [MIT LICENSE](LICENSE).
100% open-source, feel free to utilize the code however you like. 


