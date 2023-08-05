# hog

Hog helps you specify the files you want to open when looking through your Scribe logs.

[![PyPI version](https://badge.fury.io/py/scribehog.svg)](https://badge.fury.io/py/scribehog)
[![build status](https://api.travis-ci.com/endreymarcell/hog.svg?branch=master)](https://travis-ci.com/endreymarcell/hog)
[![codecov](https://codecov.io/gh/endreymarcell/hog/branch/master/graph/badge.svg)](https://codecov.io/gh/endreymarcell/hog)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


### Install

```pip3 install --upgrade scribehog```

### Usage

```hog [-v] logcategory [logfile(s)]```

`-v`: verbose logging

`logcategory`: a dash-separated list of words or word prefixes to test against the dash or underscore-separated logcategory names.  
For example: if your logcategory is called `alpha_bravo_charlie`, you can match it with `alpha-bravo-charlie`, or just `al-br-ch`, maybe even `a-b-c`, as long as it's unambigious given the list of all logcategories.  
Note that the order of the words does not matter, ie. `al-br-ch` and `ch-br-al` are the same.  

`logfile(s)`: a reference to the file or files you want to read. The default value is `-1`, meaning the most recent file. You can either use negative numbers as relative references like this, or specify a date and time in the format of `hh`, `dd-hh`, `mm-dd-hh`, or `yyyy-mm-dd-hh`. For example, you can pass `-3` for the third most recent logfile, or `10-09` for the logfile on the 10th at 9:00 AM (note the leading 0 in the hour).  
Intervals can also be specified by using a colon. Relative and absolute references can be freely mixed. When omitting a reference from either side of the colon, the end of the list is assumed, just like in Python list slicing. Examples: `-3:-2`, `10-15:10-18`, `-10:12-31-20`, `-5:`.  

You don't have to know if the specified files are gzip-compressed or not, hog takes care of that for you. The contents are uniformly printed to stdout, so you can pipe the output into `grep`, `less` or whatever you need to use.  

### Development

Make sure you have Python (>=3.5) installed.  
Clone the repository, then call `make develop`.  

![hog - Photo by Fabian Blank on Unsplash](hog.jpg)
