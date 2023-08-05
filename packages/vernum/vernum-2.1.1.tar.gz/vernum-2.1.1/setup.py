
import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__),'version')) as versionfile:
    version = versionfile.read().strip()

setup(name='vernum',
    version=version,
    description='Version numbering and git tagging for project releases',
    long_description='Version numbering and git tagging for project releases',
    url='http://gitlab.com/francispotter/vernum',
    author='Francis Potter',
    author_email='vernum@fpotter.com',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts':['vernum=vernum.__main__:run']},
    zip_safe=False)
