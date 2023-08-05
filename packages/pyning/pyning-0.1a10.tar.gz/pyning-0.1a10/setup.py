from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyning',
    version='0.1a10',
    packages=[ 'pyning' ],
    url='https://github.com/essennell/pyning',
    license='MIT',
    author='Steve Love',
    author_email='steve@arventech.com',
    description='A quick and extensible configuration management system',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers = [
                      "Programming Language :: Python :: 3",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent",
                  ],
)
