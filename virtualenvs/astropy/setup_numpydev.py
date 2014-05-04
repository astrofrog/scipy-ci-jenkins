import os
import sys
import urllib2
import subprocess
from copy import deepcopy
from distutils import version

PYTHON_VERSIONS = ['2.6', '2.7', '3.1', '3.2', '3.3', '3.4']

SCRIPT = """
# Create virtual environment
/opt/local/bin/virtualenv-{pv} -v {full}

# Install Cython
{full}/bin/pip install Cython
"""

def setup_virtualenv(versions):

    print versions['full']

    f = open('{full}.log'.format(**versions), 'w')
    code = subprocess.call(SCRIPT.format(**versions), shell=True, stdout=f, stderr=f)
    f.close()

all_versions = []

versions = {}
for python_version in PYTHON_VERSIONS:
    versions['pv'] = python_version
    versions['full'] = 'python{pv}-numpy-dev'.format(**versions)
    all_versions.append(deepcopy(versions))

from multiprocessing import Pool
p = Pool()
p.map(setup_virtualenv, all_versions)
