# genice-vpython

A [GenIce](https://github.com/vitroid/GenIce) plugin to visualize the structure with [VPython](http://vpython.org).

## Requirements

* [GenIce](https://github.com/vitroid/GenIce) >=0.23.
* [vpython](https//vpython.org) 

## Installation from PyPI

    % pip install genice-vpython

## Manual Installation

### System-wide installation

    % ./setup.py install

### Private installation

Copy the files in genice_vpython/formats/ into your local formats folder of GenIce.

## Usage

	% genice 1c -r 3 3 3 -f vpython
opens a window in the web browser to show the image.

## Options

Currently there is no option available for this plugin.

## Test in place

    % make test
