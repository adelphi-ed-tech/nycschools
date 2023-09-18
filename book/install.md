Installing Locally
==================
You can install `nycschools` for use in your own Python projects just as you would any other library, however this package also requires a local data directory to store data files.

Install `nycschools` from pypi
------------------------------
First, optionally, create a `virtualenv` then install the package with `pip`.

```bash
pip install nycschools
```

Load the data
--------------
Download the data (this might take a little bit) files by running the interactive setup script:

```bash
python -m nycschools.dataloader
```
Configure environment variables
-------------------------------
You need to set the `NYC_SCHOOLS_DATA_DIR` environment variable so
that python knows where to find the data. Where the instructions
say `/path/to/data` replace it with the full path to the
directory where you saved the data.

For example, if your username is `mxc` and you saved it into a folder
called`data` in your home folder, the full path would be something
like `C:\Users\mxc\data\school-data` on Windows or
`/Users/mxc/data/school-data` on Mac.

::::{tab-set}
:::{tab-item} Mac
:sync: tab1
On a Mac, you can set the `NYC_SCHOOLS_DATA_DIR` environment 
variable persistently by adding it to your 
`.bash_profile` file. Open a terminal window, then run:
```bash
echo 'export NYC_SCHOOLS_DATA_DIR=/path/to/data' >> ~/.bash_profile
```
Load the new settings by running:
```bash
source ~/.bash_profile
```
:::
:::{tab-item} Windows
:sync: tab2
On Windows, to set the `NYC_SCHOOLS_DATA_DIR` environment variable persistently, 
you must use the System Properties window. Here are the steps:

1. Right-click on 'This PC' or 'My Computer' and choose 'Properties'.
2. Click on 'Advanced system settings'.
3. Click on the 'Environment Variables' button.
4. Under the 'System variables' section, click 'New...' to create a new system-wide environment variable, or create a user environment variable under the "User variables" section.
5. Set the 'Variable name' to `NYC_SCHOOLS_DATA_DIR` and the 'Variable value' to the path to your data directory (e.g., `C:\path\to\data`).
6. Click 'OK' to close each window.

This will set the `NYC_SCHOOLS_DATA_DIR` environment variable permanently for the system or user, depending on where you added it.
:::
:::{tab-item} Jupyter Notebook
:sync: tab4
If you wish to set the `NYC_SCHOOLS_DATA_DIR` environment variable
directly in a Jupyter Notebook (either because Jupyter is not
reading the system variable, or you want to set or change it for one Noteboo),
you can do so using the [**env** magic command](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-env). At the top of your Notebook, in a code cell, run and execute:
```python
%env NYC_SCHOOLS_DATA_DIR=/path/to/data
```
:::
:::{tab-item} Linux
:sync: tab3
On Linux, to set the `NYC_SCHOOLS_DATA_DIR` environment variable persistently, 
you can add the export command to your `.bashrc` or `.profile` file:

To add it to .bashrc (for example), open a terminal window, then run:
```bash
echo 'export NYC_SCHOOLS_DATA_DIR=/path/to/data' >> ~/.bashrc
```
Load the new settings by running:
```bash
source ~/.bashrc
```
:::
::::
