from setuptools import setup, find_packages

def _get_requirements(path):
    reqs = None
    with open(path) as req_file:
        reqs = req_file.readlines()
    return reqs

NAME = 'pymod_init'
VERSION = '0.0.1'
REQS = _get_requirements("./requirements.txt")

setup(name=NAME,
  version=VERSION,
  packages=find_packages(include=[NAME, NAME+".*"]),
  entry_points=dict(console_scripts=['pymod-init=pymod_init.cli:init']))
