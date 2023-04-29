Installing Locally
==================
You can install `nycschools` for use in your own Python projects just as you would any other library, however this package also requires a local data directory to store data files.

First, optionally, create a `virtualenv` then install the package with `pip`.

```bash
pip install nycschools
```

Download the data files to your local project folder (where you will run you code from):

```bash
# make a local data dir
mkdir school-data

# install download and extract the 7z archive

7z x nycschools-data.7z -o./school-data/
```

```{tip}
You can install the data in any directory available with read/write access to your python
programs by setting and ENV variable to the full path to the `data_dir`

For example:

`export NYC_SCHOOLS_DATA_DIR=/opt/data/nycschools`

If you are using the library in a Jupyter Notebook, you should set either export this var
or set it in your Notebook using [the `env` magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-env), like this:

`%env NYC_SCHOOLS_DATA_DIR=~/Documents/mydataproject/school-data`

```
