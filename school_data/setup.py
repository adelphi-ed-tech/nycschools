from setuptools import find_packages, setup

setup(
    name='school_data',
    packages=find_packages(include=['school_data']),
    install_requires=["numpy","pandas","geopandas","folium","thefuzz"],
    version='0.1.0',
    description='Library for working with NYC Open Data for Public Schools',
    author='mxc',
    license='GPL',
)
