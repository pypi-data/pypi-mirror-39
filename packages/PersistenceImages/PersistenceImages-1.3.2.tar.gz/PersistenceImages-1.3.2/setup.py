import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PersistenceImages",
    version = "1.3.2",
    author = "Francis C. Motta",
    author_email = "fmotta@fau.edu",
    description = ("Functions to vectorize persistence diagrams into persistence images (see [PI] http://www.jmlr.org/papers/volume18/16-337/16-337.pdf for details)"),
    license = "MIT",
    keywords = "persistence diagrams, persistent homology, persistence images, computational topology, topological data analysis",
    url = "https://gitlab.com/csu-tda/PersistenceImages",
    packages=['PersistenceImages'],
    long_description=read('README.md'),
    classifiers=["Development Status :: 4 - Beta"]
)