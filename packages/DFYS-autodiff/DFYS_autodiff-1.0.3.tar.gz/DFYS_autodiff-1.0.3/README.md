# cs207-FinalProject 
`autodiff` 

[![Build Status](https://travis-ci.org/D-F-Y-S/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/D-F-Y-S/cs207-FinalProject)

[![Coverage Status](https://coveralls.io/repos/github/D-F-Y-S/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/D-F-Y-S/cs207-FinalProject?branch=master)

[![Doc Status](https://readthedocs.org/projects/cs207-finalproject/badge/?version=latest)](https://cs207-finalproject.readthedocs.io/en/latest/?badge=latest)


**Group Name:** DFYS

**Group Number:** 12

**Group Member:**  Feiyu Chen, Yueting Luo, Yan Zhao

### Documentation

**[Getting started](https://cs207-finalproject.readthedocs.io/en/latest/Getting%20Started.html) and see the full documentation on [Read the Docs](https://cs207-finalproject.readthedocs.io/en/latest/)**

### Quick Installation Guide

#### Install Through PyPI

The easiest way to install `autodiff` is by `pip`. In the command line, type in:

```
pip install DFYS-autodiff
```

#### Install Manually

The user can choose to install `autodiff` directly from the source in this repository. We suppose that the user has already installed `pip` and `virtualenv`:

1. clone the project repo by `git clone git@github.com:D-F-Y-S/cs207-FinalProject.git`
2. `cd` into the local repo and create a virtual environment by `virtualenv env` 
3. activate the virtual environment by `source env/bin/activate` (use `deactivate` to deactivate the virtual environment later.)
4. install the dependencies by `pip install -r requirements.txt`
5. install `autodiff` by `pip install -e .`


### Testing

```
pytest --pyargs DFYS-autodiff
```