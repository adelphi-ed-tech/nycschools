import os
from nycschools import config
from invoke import task

@task
def make_archive(c):
    """Create a .7z archive of all of the files in the data directory."""

    data_dir = os.path.abspath(config.  data_dir)
    filename = config.urls["school-data-archive"].filename
    print("removing existing archive", filename)
    c.run(f"rm -f {filename}")
    print(f"creating archive {filename} from {data_dir}/*")
    c.run(f"7z a {filename} {data_dir}/*")


@task
def build(c):
    """Build the package."""
    c.run("python -m build")

@task
def test(c):
    """Run unit tests."""
    c.run("pytest")

@task
def docs(c):
    """Build the documentation with sphynx."""
    c.run("sphinx-apidoc nycschools -o docs/api")
    c.run("sphinx-build -b html docs docs/build")