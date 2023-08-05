import io
import os
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'opencmiss', 'utils', '__init__.py')) as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)
readme.append('License')
readme.append('=======')
readme.append('')
readme.append('')
requires = ['opencmiss.zinc']
software_licence = readfile("LICENSE")

setup(
    name='opencmiss.utils',
    version=version,
    description='OpenCMISS Utilities for Python.',
    long_description='\n'.join(readme) + software_licence,
    classifiers=[],
    author='Hugh Sorby',
    author_email='h.sorby@auckland.ac.nz',
    url='https://github.com/OpenCMISS-Bindings/opencmiss.utils',
    license='Apache Software License',
    packages=find_packages(exclude=['ez_setup',]),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)

