Installation
============

Installing in Google Colab
---------------------------
### Link to the data resources from your Google Drive
1. Sign into your Google Account
2. Open the link to our source data files: <https://drive.google.com/drive/folders/1Yf7ZbK0S8HyYR7kL9_MUNePWj6a7GwbL?usp=share_link>
3. Create a shortcut to the data in your drive

<img src="_static/add-gdrive.gif" alt="menu navigating to add link to gdrive">

### Importing to Colab
Open a new Colab notebook and then add this code at the start of your program:

```bash
# install the package and its requirements
!pip install nycschools
```
```python
# discover the data in your Google Drive, or download it to the local Colab
# if no suitable data is found
from nycschools import dataloader
dataloader.download_data()
```

The `dataloader` will prompt you for permission to look in your Google Drive for the data folder. If you do not allow access, the program will attempt to download the data locally. You will have to download the data for each session when using this notebook.

Installing locally
------------------
Optionally, create a `virtualenv` then install with `pip`

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

Installing with `invoke`
------------------------

First, create a `virtualenv` for the project using [python](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment),
[conda](https://docs.conda.io/projects/conda/en/latest/commands/create.html),
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html), or whichever manner you choose.

Once it's created, make sure your `venv` is active. This project uses the [invoke](https://www.pyinvoke.org/) task runner to automate development tasks, and we'll use it to establish your environment. At this time, the tasks are configured to work in a linux (and probably mac osx) environment.

```bash
# clone the repository
git clone https://github.com/adelphi-ed-tech/nycschools.git
cd nycschools

# install the development requirements
pip install -r requirements.txt

# run the development install task
invoke install-dev
```

Manual dev install
------------------
If `invoke` isn't working for you or you are setting up on windows, you can get up and running with these steps:

1. Get the repo: `git clone https://github.com/adelphi-ed-tech/nycschools.git`
2. Move into the project directory.
3. Create a `venv` for your project.
4. Install the project requirements with `pip` or `conda`. These are found in `requirements.txt`
5. Install the library from source in development mode: `pip install -e nycschools`
6. Download the data from: <https://drive.google.com/file/d/1I35Wr1-UObcPm9CYSgqPUa8JOzOuAQBF/view?usp=share_link>
7. Create a new folder called `nyc-schools` and extract the contents of  `nycschools-data.7z` into `nyc-schools`



