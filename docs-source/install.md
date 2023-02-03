Installation
============
This alpha version of the software is not available via PyPi, however you
can download and build the `nycschools` package yourself. This process
has been (lightly) tested in Ubuntu and Pop_OS.

### Set up your environment
- (optional) create a virtual environment for working with nyc schools
- [install `python build`](https://pypi.org/project/build/)
- [clone or download the source from github](https://github.com/adelphi-ed-tech/nycschools)

### Build the project
Open a terminal and move into the `nycschools` project folder. Activate
your virtualenv if using one.

Install Python dependencies with:
~~~~~~{.bash}
pip install -r requirements.txt
~~~~~~

Build the Project with:
~~~~~~{.bash}
python -m build
~~~~~~

Install the package with:
~~~~~~{.bash}
pip install dist/nycschools-0.1.0.tar.gz
~~~~~~

### Configure the project
_coming soon: set data dir_

### (optional) Download the data
The first time you load the data from the live data portals
can be very slow. The NYSED data in particular can load
slowly, especially on an older computer or over a low internet
connection.

The core data files are included with the git project, so you can
speed up development by copying the contents of the `data` directory
into the `nycschools` data dir on your machine. To find this directory
run:

~~~~~~{.bash}
python -m nycschools.dataloader
~~~~~~

## Development environment
If you wish to build and develop the source code, follow these instructions after enabling your `venv`:

~~~~~~{.bash}
# install all libraries
pip install -r dev-requirements.txt
# install dev version of project
pip install -e .
# run unit tests
pytest
~~~~~~


### (optional) Test the code
Run the unit tests to make sure everything is up and running.
Running these tests will also download all of the data files
from their online sources.
~~~~~~{.bash}
pytest
~~~~~~
