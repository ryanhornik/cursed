#!/usr/bin/env python3

import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('tests')
    runner = unittest.TextTestRunner(verbosity=1)

    result = runner.run(suite)
    if len(result.errors) > 0:
        exit(3)
    if len(result.failures) > 0:
        exit(2)
