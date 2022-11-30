New York Schools Open Data Project
==================================

The mission of the NYC Schools Open Data Project is to make open data regarding public schools in New York available to everyone interested in improving our schools, regardless of their technical background or familiarity with data analysis. We believe that fighting for educational equity requires us to broaden the audience of who can use and analyze data. Accordingly, we want to make educational data more accessible, train people to use it, and demystify and remove the barriers to access.

Our goal is to build platform where any motivated individual or groups can evaluate available school data, interpret it to help understand issues they care about, and employ data as part of larger arguments in our conversations about schools in New York.

**[Find technical documentation and examples here](https://adelphi-ed-tech.github.io/nycschools/)**

Join our Jupyter Hub
--------------------
As our goal is make it easier to work with the data, we maintain a
[Jupyter Hub](https://jupyter.org/hub) with all of the necessary libraries
and data sets so that you can dive in and start playing with the data
without having to install anything except a web browser on your computer.

At this stage in development, the hub is invitation only. Please contact
Matt for an invitation.

Installation
------------
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

### (optinoa) Test the code
Run the unit tests to make sure everything is up and running.
Running these tests will also download all of the data files
from their online sources.
~~~~~~{.bash}
pytest
~~~~~~
