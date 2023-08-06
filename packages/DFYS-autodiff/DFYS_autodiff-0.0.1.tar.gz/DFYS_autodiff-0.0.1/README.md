# cs207-FinalProject
`autodiff`
by

Feiyu Chen, Yan Zhao, Yueting Luo

[![Build Status](https://travis-ci.org/D-Y-F-S/cs207-FinalProject.svg?branch=master)](https://travis-ci.org/D-Y-F-S/cs207-FinalProject)

[![Coverage Status](https://coveralls.io/repos/github/D-Y-F-S/cs207-FinalProject/badge.svg?branch=master)](https://coveralls.io/github/D-Y-F-S/cs207-FinalProject?branch=master)

## Introduction
Automatic differentiation (AD) is a family of techniques for efficiently and accurately evaluating derivatives of numeric functions expressed as computer programs. Application of AD includes Newton’s method for solving nonlinear equations, real-parameter optimization, probabilistic inference, and backpropagation in neural networks. AD has been extremely popular because of the booming development in machine learning and deep learning techniques. Our AD sofeware package enable user to calculate derivatives using the forward and reverse mode.

## Installing `autodiff`
Here is how to install `autodiff` on command line. We suppose that the user has already installed `pip` and `virtualenv`:
1. clone the project repo by `git clone git@github.com:D-Y-F-S/cs207-FinalProject.git`
2. `cd` into the local repo and create a virtual environment by `virtualenv env` 
3. activate the virtual environment by `source env/bin/activate` (use `deactivate` to deactivate the virtual environment later.)
4. install the dependencies by `pip install -r requirements.txt`
5. install `autodiff` by `pip install -e .`

## Getting Started
See `milestone2.ipynb` under `docs/`.