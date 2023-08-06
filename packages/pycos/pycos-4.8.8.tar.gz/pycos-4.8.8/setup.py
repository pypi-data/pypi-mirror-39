import sys
import os
import re
import shutil
import subprocess
from setuptools import setup

if sys.version_info.major == 3:
    if sys.version_info.minor >= 7:
        base_dir = 'py3.7'
    else:
        base_dir = 'py3'
else:
    assert sys.version_info.major == 2
    assert sys.version_info.minor >= 7
    base_dir = 'py2'

shutil.rmtree('py3.7', ignore_errors=True)
shutil.copytree('py3', 'py3.7')
base_path = os.path.join('py3.7', 'pycos')
for path in [base_path, os.path.join(base_path, 'examples')]:
    for filename in os.listdir(path):
        if filename.endswith('.py'):
            subprocess.call('sed -i "s/raise StopIteration/return/" %s' %
                            os.path.join(path, filename), shell=True)

with open(os.path.join(base_dir, 'pycos', '__init__.py')) as fd:
    regex = re.compile(r'^__version__ = "([\d\.]+)"$')
    for line in fd:
        match = regex.match(line)
        if match:
            module_version = match.group(1)
            break

setup(
    name='pycos',
    version=module_version,
    description='Concurrent, Asynchronous, Distributed, Communicating Tasks with Python',
    long_description=open('README.rst').read(),
    keywords='concurrency, asynchronous, network programming, distributed, tasks, message passing',
    url='http://pycos.sourceforge.io',
    author='Giridhar Pemmasani',
    author_email='pgiri@yahoo.com',
    package_dir={'':base_dir},
    packages=['pycos'],
    package_data = {
        'pycos' : ['data/*', 'doc/*', 'examples/*'],
    },
    scripts=[os.path.join(base_dir, 'pycos', script)
             for script in ['dispycos.py', 'dispycosnode.py']],
    license='Apache 2.0',
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        ]
    )
