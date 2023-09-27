Development Install
===================
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
5. Install the library from source in development mode: `pip install -e .[dev]`
6. Download the data from: <https://drive.google.com/file/d/1I35Wr1-UObcPm9CYSgqPUa8JOzOuAQBF/view?usp=share_link>
7. Create a new folder called `nyc-schools` and extract the contents of  `nycschools-data.7z` into `nyc-schools`
8. Follow the directions from the [regular install](install.md) to configure environment variables.



