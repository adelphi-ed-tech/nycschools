import os
import toml

from nycschools import config
from invoke import task


def get_project_config():
    config = {}
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)
    return config["project"]

@task
def archive(c):
    """Create a .7z archive of all of the files in the data directory."""
    
    print("Creating a .7z archive of all of the files in the data directory.")

    data_dir = os.path.abspath(config.  data_dir)
    filename = config.urls["school-data-archive"].filename
    print("removing existing archive", filename)
    c.run(f"rm -f {filename}")
    print(f"creating archive {filename} from {data_dir}/*")
    c.run(f"7z a {filename} {data_dir}/*")


@task
def build(c):
    """Build the package."""
    project = get_project_config()
    print(f"building {project['name']} v{project['version']} ")
    c.run("rm -rf dist")
    c.run("python -m build")

@task
def push(c, test=True):
    """Build the package."""
    if test:
        print("pushing to testpypi")
        c.run("twine upload --repository testpypi dist/*")
    else:
        print("pushing to pypi. this is NOT a drill.")
        c.run("twine upload dist/*")
    

@task
def test(c, opt=""):
    """Run unit tests."""
    c.run(f"pytest {opt}")

@task
def docs(c):
    """Build the documentation with sphynx."""
    c.run("sphinx-apidoc nycschools -o docs-source/api")
    c.run("sphinx-build -b html docs-source docs")