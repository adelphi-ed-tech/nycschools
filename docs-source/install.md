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

```python
# install the package and its requirements
!pip install nycschools

# discover the data in your Google Drive, or download it to the local Colab
# if no suitable data is found
from nyschools import dataloader
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
mkdir school-data
wget https://drive.google.com/file/d/1I35Wr1-UObcPm9CYSgqPUa8JOzOuAQBF/view?usp=share_link
7z x nycschools-data.7z -o./school-data/
```

```{tip}
You can install the data in any directory available with read/write access to your python
programs by setting and ENV variable to the full path to the `data_dir`

For example:

`export NYC_SCHOOLS_DATA_DIR=/opt/data/nycschools`
```

Installing for development
--------------------------

First, create a `virtualenv` for the project. Activate the `venv`.

```bash
# clone the repository
git clone https://github.com/adelphi-ed-tech/nycschools.git

# install the development environment
pip install -r requirements.txt

# get the data
mkdir school-data
wget https://drive.google.com/file/d/1I35Wr1-UObcPm9CYSgqPUa8JOzOuAQBF/view?usp=share_link
7z x nycschools-data.7z -o./school-data/

# build the project
invoke build

# install `nycschools` in dev mode
pip install -e dist/nycschools-latest.tar.gz

# build the docs
invoke docs -c

# run unit tests
invoke test
```
