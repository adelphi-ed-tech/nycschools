import os
from nycschools import config
from invoke import task

@task
def archive(c):
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
def test(c, opt=""):
    """Run unit tests."""
    c.run(f"pytest {opt}")

@task
def docs(c):
    """Build the documentation with sphynx."""
    c.run("sphinx-apidoc nycschools -o docs-source/api")
    # c.run("rsync -r docs-source/res docs/res")
    c.run("sphinx-build -b html docs-source docs")