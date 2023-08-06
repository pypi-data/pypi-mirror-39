#!/usr/bin/env python
"""Utility functions and classes for python"""
########################################################################
# File: utils.py
#  executable: utils.py
#
# Author: Andrew Bailey
# History: 12/09/17 Created
########################################################################

import logging
import os
import json
from datetime import datetime
from contextlib import contextmanager
from io import StringIO
import sys


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def create_logger(file_path, name="a", info=False, debug=False):
    """Create a logger instance which will write all logs to file path and display logs at requested level
    :param file_path: path to file without .log extension
    :param name: unique name of logger
    :param info: set logging level to INFO
    :param debug: set logging level to DEBUG
    :return: logger which will write all log calls to file and display at level requested
    """
    assert type(info) is bool, "info should be bool, you passed {}".format(type(info))
    assert type(debug) is bool, "debug should be bool, you passed {}".format(type(debug))
    assert type(file_path) is str, "file path needs to be string"
    assert type(name) is str, "name needs to be string"

    level = logging.WARNING
    if debug:
        level = logging.DEBUG
    if info:
        level = logging.INFO
    # create name for logger
    root_logger = logging.getLogger(name)
    root_logger.setLevel(logging.DEBUG)
    # format log info formatting
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

    file_handler = logging.FileHandler("{}.log".format(file_path))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return logging.getLogger(name)


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def list_dir(path, ext=""):
    """get all file paths from local directory with extension
    :param path: path to directory
    :type ext: str
    :type path: str
    :return: list of paths to files
    """
    assert type(path) is str, "Path must be a string"
    assert os.path.isdir(path), "Path does not exist"
    if ext == "":
        only_files = [os.path.join(os.path.abspath(path), f) for f in
                      os.listdir(path) if
                      os.path.isfile(os.path.join(os.path.abspath(path), f))]
    else:
        only_files = [os.path.join(os.path.abspath(path), f) for f in
                      os.listdir(path) if
                      os.path.isfile(os.path.join(os.path.abspath(path), f))
                      if f.split(".")[-1] == ext]
    return only_files


def load_json(path):
    """Load a json file and make sure that path exists"""
    path = os.path.abspath(path)
    assert os.path.isfile(path), "Json file does not exist: {}".format(path)
    with open(path) as json_file:
        args = json.load(json_file)
    return args


def save_json(dict1, path):
    """Save a python object as a json file"""
    path = os.path.abspath(path)
    with open(path, 'w') as outfile:
        json.dump(dict1, outfile)
    assert os.path.isfile(path)
    return path


def time_it(func, *args):
    """Very basic timing function
    :param func: callable function
    :param args: arguments to pass to function
    :return: object returned from function, time to complete
    """
    assert callable(func), "Function is not callable"
    start = datetime.now()
    something = func(*args)
    end = datetime.now()
    return something, end - start


def debug(verbose=False):
    """Method for setting log statements with verbose or not verbose"""
    assert type(verbose) is bool, "Verbose needs to be a boolean"
    if verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")
        logging.info("This should not print.")


if __name__ == '__main__':
    print("This is a library of python functions")
