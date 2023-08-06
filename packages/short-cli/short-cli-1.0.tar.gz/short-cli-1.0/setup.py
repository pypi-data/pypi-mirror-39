from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='short-cli',    # This is the name of your PyPI-package.
    version='1.0',                          # Update the version number for new releases
    description='Shorten and track URLs from the command line',
    url='http://github.com/Clocktapus/short-cli',
    author='Max Beyer',
    author_email='mwbpenguin@gmail.com',
    license='MIT',
    install_requires=[
          'bs4',
          'requests',
      ],
    packages=['short']
)
