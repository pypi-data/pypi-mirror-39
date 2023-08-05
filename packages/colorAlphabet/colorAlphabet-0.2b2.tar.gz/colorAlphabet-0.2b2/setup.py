from setuptools import setup, find_packages
# setuptools allows "python setup.py develop"
import os
import subprocess
from pip.req import parse_requirements
from pip.download import PipSession

import colorAlphabet

#------------------------------------------------------------------------------
def _get_version_tag():
    """ Talk to git and find out the tag/hash of our latest commit
    """
    try:
        p = subprocess.Popen(["git", "describe", "--abbrev=0", ],
                             stdout=subprocess.PIPE)
    except EnvironmentError as e:
        print("Couldn't run git to get a version number for setup.py")
        print('Using current version "%s"' % colorAlphabet.__version__ )
        return colorAlphabet.__version__
    version = p.communicate()[0].strip().decode()
    with open(os.path.join("colorAlphabet", "__version__.py"), 'w') as the_file:
        the_file.write('__version__ = "%s"\n' % version)
    return version

#------------------------------------------------------------------------------
reqfile = "requirements.txt"

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [str(ir.req)
        for ir in parse_requirements(reqfile, session=PipSession())]

setup(name='colorAlphabet',
    version=_get_version_tag(),
    install_requires=requirements,
    author='Roberto Vidmar',
    author_email="rvidmar@inogs.it",
    description=('Use Paul Green-Armytage color alphabet to color text output'
            ' to a terminal'),
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/bvidmar/colorAlphabet',
    packages=find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ),
    )
