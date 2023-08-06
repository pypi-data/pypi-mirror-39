import codecs
import os
import re
from setuptools import find_packages, setup, Command


here = os.path.dirname(os.path.abspath(__file__))
version = '0.0.0'
description = (
    "This library currently implements the features released under "
    "version 3.0.1 of OANDA's REST API."
)
changes = os.path.join(here, "CHANGES.rst")
pattern = r'^(?P<version>[0-9]+.[0-9]+(.[0-9]+)?)'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        match = re.match(pattern, line)
        if match:
            version = match.group("version")
            break


# Save last Version
def save_version():
    version_path = os.path.join(here, "oandapy/version.py")

    with open(version_path) as version_file_read:
        content_file = version_file_read.read()

    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, content_file, re.M)
    current_version = mo.group(1)

    content_file = content_file.replace(current_version, "{}".format(version))

    with open(version_path, 'w') as version_file_write:
        version_file_write.write(content_file)


save_version()


class VersionCommand(Command):
    description = 'Show library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


# Get the long description
with codecs.open(os.path.join(here, 'README.rst')) as f:
    long_description = '\n{}'.format(f.read())

# Get change log
with codecs.open(os.path.join(here, 'CHANGES.rst')) as f:
    changelog = f.read()
    long_description += '\n\n{}'.format(changelog)

# Requirements
with codecs.open(os.path.join(here, 'requirements.txt')) as f:
    install_requirements = [line.split('#')[0].strip() for line in f.readlines() if not line.startswith('#')]

with codecs.open(os.path.join(here, 'requirements-dev.txt')) as f:
    tests_requirements = [line.replace('\n', '') for line in f.readlines() if not line == '-r requirements.txt\n']


setup(
    author='Rafael Henter, Gustavo Ferreira',
    author_email='rafael@henter.com.br',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    cmdclass={'version': VersionCommand},
    description=description,
    install_requires=install_requirements,
    keywords='translate translation command line',
    license='MIT',
    long_description=long_description,
    name='oandapy',
    packages=find_packages(exclude=['docs', 'tests', 'tests.*', 'requirements']),
    setup_requires=['pytest-runner'],
    tests_require=tests_requirements,
    url='https://github.com/rhenter/oandapy',
    version=version,
)
