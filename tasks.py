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
def clean(c):
    """Remove dist and docs directories."""
    c.run("rm -rf dist")
    c.run("rm -rf docs")

@task
def build(c):
    """Build the package."""
    project = get_project_config()
    print(f"building {project['name']} v{project['version']} ")
    c.run("rm -rf dist")
    c.run("python -m build")
    c.run(f"cp dist/nycschools-{project['version']}.tar.gz dist/nycschools-latest.tar.gz")

@task
def push(c, production=False):
    """Push the current distribution to pypi.
    By default, this pushes to testpypi.
    To push to pypi, use the -p or --production flag.
    """
    if production:
        print("Pushing to pypi. This is NOT A DRILL.")
        c.run("twine upload dist/*")
    else:
        print("Pushing to testpypi")
        c.run("twine upload --repository testpypi dist/*")
    

@task
def test(c, opt=""):
    """Run unit tests."""
    c.run(f"pytest {opt}")

@task
def docs(c, clean=False):
    """Build the documentation with sphynx."""
    if clean:
        c.run("rm -rf docs")
    c.run("sphinx-apidoc nycschools -o docs-source/api")
    c.run("sphinx-build -b html docs-source docs")

@task
def install_from_testpypi(c):
    """Install the package from testpypi but using real pypi for dependencies."""
    c.run("python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nycschools")


@task
def tag(c):
    """Tag the current version."""
    project = get_project_config()
    version = project["version"]
    c.run(f"git tag -a {version} -m 'version {version}'")
    c.run(f"git push --tags")