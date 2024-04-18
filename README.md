# H5View

_A small app for viewing h5 files in a simple and clean way_

<p align="center"><img src="https://github.com/refeyn/h5view/assets/103422031/7687cfb1-12e3-4e1c-b6ff-c45456ef91b4" width="40%"> <img src="https://github.com/refeyn/h5view/assets/103422031/b3f326fb-6f09-4cc2-b5a1-6949130292b7" width="40%"></p>

Features:

 - Can open and view datasets of any HDF5 files h5py can read
 - Navigate hierarchical groups using a simple tree view
 - Can render >=1D data as tables
 - Can render >=2D data as images
 - Sensible display of strings and other 0D data
 - Displays dataset attributes and metadata (size, datatype, compression filters, etc.)

# Installation

Executable versions of this tool can be found under the releases tab on GitHub. Alternatively, h5view can be installed by pip (`pip install h5view`) and then run using the `h5view` command.

# Development

## Run from source

 - Clone this repo.
 - Run `setup_venv.ps1` to create the virtual env (subsequent runs only need `activate_venv.ps1`).
 - Run `python -m h5view` to run the app.

## Develop

 - Clone this repo.
 - Run `setup_venv.ps1` to create the virtual env.
 - Open the workspace is VSCode.
 - Select the venv in the venv menu.
 - The ui conversion is run automatically before running the app.

## Build executable

 - Run `build.ps1`
