from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='nycschools',
    version='0.1.0',
    packages=['nycschools'],
    description="Tools to work with open data about New York City public schools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adelphi-ed-tech/nycschools",
    author="Matthew X. Curinga",
    author_email="matt@curinga.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Framework :: Jupyter',
        'Topic :: Education',
    ],
    keywords="opendata, schools, newyorkcity",
    python_requires=">=3.7",
    package_data={
        'dataurls': ['dataurls.json']
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/adelphi-ed-tech/nycschools/issues",
        "Source": "https://github.com/adelphi-ed-tech/nycschools"
    },

)
