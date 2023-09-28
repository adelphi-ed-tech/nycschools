import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
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
def serve_docs(c):
    """Serve the documentation locally."""
    print("Starting jupyter book server at http://localhost:8000")
    c.run("python -m http.server --directory book/_build/html")
    # run server from python
    # os.chdir("book/_build/html")
    # server_address = ('', 8000)
    # httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    # httpd.serve_forever()

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
    dataloader.download_data("school-data")
    dataloader.set_env_var("NYC_SCHOOLS_DATA_DIR", "school-data")
    print(f"""
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


@task
def rebuild_docs(c):
    """Rebuild the documentation."""
    
    print("Rebuilding the API docs.")
    api(c, clean=True)
    print("Rebuilding the documentation.")
    book(c, clean=True, docs=True)


@task
def full_release(c):
    """Perform a full release of the package."""
    print("Performing a full release of the package.")

    print("Running tests.")
    test(c)

    print("Building the package.")
    build(c)

    print("Creating archive with latest data.")
    archive(c)

    print("Rebuilding the documentation.")
    rebuild_docs(c)
    
    print("Pushing to pypi.")
    push(c, production=True)

    print("Tagging the release.")
    tag(c)
