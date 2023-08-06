"""A setuptools based setup module"""
from setuptools import setup, find_packages

PACKAGES = find_packages()
PACKAGES.append('gui')
PACKAGES.append('misc')

setup(
	name = "robot-data-visualizer",
	version = "0.3",
	url='https://github.com/klatimer/robot-data-visualizer',
	license='MIT',
	packages=PACKAGES,
	author='Ray Adler, Ken Latimer, Hao Wu, Robin Li',
	author_email='wh1210@uw.edu',
	requires=['numpy','matplotlib','staticmap','scipy'],
	install_requires=['numpy','matplotlib','staticmap','scipy']
)
