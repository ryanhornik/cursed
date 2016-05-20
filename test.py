#!/usr/bin/env python3

import unittest
import coverage

if __name__ == "__main__":
    from sys import argv
    module = argv[1] if len(argv) > 1 else ''

    cov = coverage.Coverage(
        source=[module if module else '.'],
        omit=['tests/*', 'test.py'],
        branch=True
    )

    suite = unittest.TestLoader().discover('tests.{}'.format(module) if module else 'tests')
    runner = unittest.TextTestRunner(verbosity=1)

    cov.start()
    runner.run(suite)
    cov.stop()

    cov.html_report(directory='htmlcov_{}'.format(module) if module else 'htmlcov_all')
