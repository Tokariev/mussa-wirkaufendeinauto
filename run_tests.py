
import os

# Tested in Python 3.8
# https://docs.python.org/3/library/unittest.html#module-unittest
from unittest import TestLoader, TestResult
from pathlib import Path


def run_tests():
    print('Running tests...')
    test_loader = TestLoader()
    test_result = TestResult()

    # Use resolve() to get an absolute path
    # https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve
    test_directory = str(Path(__file__).resolve().parent / 'tests')
    print(test_directory)
    test_suite = test_loader.discover(test_directory, pattern='Test*.py')
    test_suite.run(result=test_result)

    # See the docs for details on the TestResult object
    # https://docs.python.org/3/library/unittest.html#unittest.TestResult

    if test_result.wasSuccessful():
        print('All tests passed!')
        # exit(0)
    else:
        # Here you can either print or log your test errors and failures
        # test_result.errors or test_result.failures
        print(test_result.failures)
        exit(-1)

if __name__ == '__main__':
    run_tests()
