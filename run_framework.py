import os

from behave.__main__ import main as behave_main

# add options handling. Config file!

behave_main("test/features")
