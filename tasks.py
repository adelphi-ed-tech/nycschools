import os
import toml
from functools import wraps
from dotenv import load_dotenv

from nycschools import config, dataloader
from invoke import task


def get_project_config():
    config = {}
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)
    return config["project"]



def with_env(func):
    """Decorator to wrap a task after ENV vars are read, including data_dir."""
    @task
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Initializing the project.")
        load_dotenv()
        print(os.getenv("NYC_SCHOOLS_DATA_DIR"))
        print("wrapping", func.__name__)
        return func(*args, **kwargs)
    return wrapper


@with_env
def dummy(c, foo=None, bar=None):
    """Dummy task."""
    print("dummy task")


@task
def archive(c):
    """Create a .7z archive of all of the files in the data directory."""
    
    print("Creating a .7z archive of all of the files in the data directory.")

    data_dir = os.path.abspath(config.data_dir)
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
    project = get_project_config()
    current = f"nycschools-{project['version']}"
    if production:
        print("Pushing to pypi. This is NOT A DRILL.")
        c.run(f"twine upload dist/{current}*")
    else:
        print("Pushing to testpypi")
        c.run(f"twine upload --repository testpypi dist/{current}*")
    

@task
def test(c, opt=""):
    """Run unit tests."""
    c.run(f"pytest {opt}")


@task
def api(c, clean=False):
    """Build the api documentation with sphynx-apidoc."""
    if clean:
        c.run("rm -rf book/api")
    c.run("sphinx-apidoc nycschools -o book/api")


@with_env
def book(c, clean=False, docs=False):
    """Build the documentation with sphinx."""
    if clean:
        c.run("rm -rf book/_build")
        api(c)
    c.run("jupyter-book build book")
    if docs:
        print("copying book/_build/html to docs for github pages")
        c.run("cp -r book/_build/html/* docs")
        c.run("touch docs/.nojekyll")


@task
def toc(c):
    """Generate table of content files for each
    folder in book/nb."""

    sections = sorted(os.listdir("book/nb"))

    for section in sections:
        if not os.path.isdir(f"book/nb/{section}"):
            continue
        print(f"""
  - caption: {section[3:].replace("-", " ")}
    chapters:""")
        files = os.listdir(f"book/nb/{section}")
        files = ["index.mb"] + sorted([f for f in files if f.endswith(".ipynb") and f[0] not in "._"])
        for f in files:
            print(f"    - file: nb/{section}/{f}")

@task
def install_from_testpypi(c):
    """Install the package from testpypi but using real pypi for dependencies."""
    c.run("python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple nycschools")

@task
def install_dev(c):
    """Install a new development environment."""

    print("Installing a new development environment.")

    print("Installing nycschools in editable/development mode")
    c.run("pip install -e .[dev]")

    print("Downloading data to local directory 'school-data'")
    dataloader.download_archive("school-data")
    pwd = os.getcwd()
    data_dir = os.path.join(pwd, "school-data")
    print("Writing .env file with NYC_SCHOOLS_DATA_DIR")
    c.run(f"echo 'NYC_SCHOOLS_DATA_DIR={data_dir}' > .env")
    print(f"""To complete the installation, you can set the
NYC_SCHOOLS_DATA_DIR environment variable to {data_dir} by
adding the following line to your .bashrc or .zshrc file:
export NYC_SCHOOLS_DATA_DIR={data_dir}

Installation complete. Run 
invoke --list 
to see available tasks.
""")

@task
def tag(c):
    """Tag the current version."""
    project = get_project_config()
    version = project["version"]
    c.run(f"git tag -a {version} -m 'version {version}'")
    c.run(f"git push --tags")

@task
def download_data(c):
    """Download the data from the NYC Open Data Portal."""
    print("Downloading data to local directory 'school-data'")
    dataloader.download_archive("school-data")
