#!/usr/bin/env python3

import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('tests')
    runner = unittest.TextTestRunner(verbosity=1)

    runner.run(suite)
