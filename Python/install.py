import os
import shutil
import urllib2

SETUPTOOLS_VERSION = "1.1.6"
VIRTUALENV_VERSION = "1.9.1"
PIP_VERSION = "1.3.1"

PYTHON_URL = "http://www.python.org/ftp/python/{version}/Python-{version}.{ext}"
SETUPTOOLS_URL = "https://pypi.python.org/packages/source/s/setuptools/setuptools-{sv}.tar.gz".format(sv=SETUPTOOLS_VERSION)
VIRTUALENV_URL = " https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{vv}.tar.gz".format(vv=VIRTUALENV_VERSION)

PIP_URL = "https://pypi.python.org/packages/source/p/pip/pip-{pv}.tar.gz".format(pv=PIP_VERSION)

def download(url):
    print url
    u = urllib2.urlopen(url)
    f = open(os.path.basename(url), 'wb')
    f.write(u.read())
    f.close()
    if url.endswith('bz2'):
        os.system('tar xvjf {filename}'.format(filename=os.path.basename(url)))
    else:
        os.system('tar xvzf {filename}'.format(filename=os.path.basename(url)))

EXTENSION = {}
EXTENSION['2.6.8'] = 'tgz'
EXTENSION['2.7.5'] = 'tgz'
EXTENSION['3.1.5'] = 'tgz'
EXTENSION['3.2.5'] = 'tar.bz2'
EXTENSION['3.3.2'] = 'tar.bz2'

for version in ['2.6.8', '2.7.5', '3.1.5', '3.2.5', '3.3.2']:

    short_version = version[:3]

    if os.path.exists('Python-{version}'.format(version=version)):
        shutil.rmtree('Python-{version}'.format(version=version))

    download(PYTHON_URL.format(version=version, ext=EXTENSION[version]))

    os.chdir('Python-{version}'.format(version=version))
    os.system('./configure --prefix=$HOME/usr/python ; make ; make install')
    os.chdir('..')

    shutil.rmtree('Python-{0:s}'.format(version))

    if os.path.exists('setuptools-{sv}'.format(sv=SETUPTOOLS_VERSION)):
        shutil.rmtree('setuptools-{sv}'.format(sv=SETUPTOOLS_VERSION))

    download(SETUPTOOLS_URL)

    os.chdir('setuptools-{sv}'.format(sv=SETUPTOOLS_VERSION))
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('setuptools-{sv}'.format(sv=SETUPTOOLS_VERSION))

    if os.path.exists('pip-{pipv}'.format(pipv=PIP_VERSION)):
        shutil.rmtree('pip-{pipv}'.format(pipv=PIP_VERSION))

    download(PIP_URL)

    os.chdir('pip-{pipv}'.format(pipv=PIP_VERSION))
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('pip-{pipv}'.format(pipv=PIP_VERSION))

    # Need to use virtualenv 1.9.1 because it includes pip 1.3.1 which works with Python 3.1
    os.system('$HOME/usr/python/bin/pip-{0:s} install {1:s} --upgrade --force'.format(short_version, VIRTUALENV_URL))
