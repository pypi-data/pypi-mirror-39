from setuptools import setup, find_packages
import pydial
import os


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


# PROJECT REQUIREMENTS -------------------------------------------------------------------------------
requirements = [
    'eulxml>=1.0.1',
    'eulfedora',
    'pymarc',
    'lxml',
    'jsonschema',
    'six',
]

setup(
    name='pydial',
    version=pydial.__version__,
    url='https://gitlab.sisg.ucl.ac.be/bibsys/pydial',
    license='https://opensource.org/licenses/MIT',
    author='michotter',
    author_email='renaud.michotte@uclouvain.be',
    description='Use DIAL Object with Python',
    long_description=read('README.rst'),
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True
)
