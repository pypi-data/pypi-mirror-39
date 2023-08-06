# AutoDiffX - A Graph-Based Automatic Differentiation Package

[![Build Status](https://travis-ci.org/CS207-Project-Team-1/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/CS207-Project-Team-1/cs207-FinalProject)
[![Coverage Status](https://coveralls.io/repos/github/CS207-Project-Team-1/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/CS207-Project-Team-1/cs207-FinalProject?branch=master)

This is our CS207 Final Project implementing Automatic Differentiation. Our group has the following members:

* Hanyu Jiang
* Hugo Ramambason
* William Fu

## Installing and Setup

### Installing from Source

If you want the latest nightly version of AutoDiffX, clone from our github
repository and install the latest version directly.

```bash
git clone https://github.com/CS207-Project-Team-1/cs207-FinalProject autodiffx
cd autodiffx
pip install -r requirements.txt
python3 setup.py install
```

If you are working on a python virtual environment or Mac OSX or your user's
python distribution, this should work. If editing the system python, you may
need to run the last command with root permissions by adding `sudo`.

### Installing from pip

For the stable version, you can install our package from PyPI.

```bash
pip install autodiffx
```

You can also install the nightly version from our Github using pip.

```bash
pip install git+https://github.com/CS207-Project-Team-1/cs207-FinalProject
```

## Testing

All of the tests are run using pytest. To run pytest, you want to be in the
root directory of the repository. To ensure that `pytest` gets the imports
correct, you want to run it such that it adds the current path to `PYTHONPATH`.
The easiest way to do so is:

```bash
python -m pytest
```

This should run all of the tests for the package.
