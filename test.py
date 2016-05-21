#!/usr/bin/env python3

import unittest
import coverage

if __name__ == "__main__":
    from sys import argv

    cov = coverage.Coverage(
        source=['.'],
        omit=['tests/*', 'test.py'],
        branch=True
    )

    suite = unittest.TestLoader().discover('tests')
    runner = unittest.TextTestRunner(verbosity=1)

    cov.start()
    runner.run(suite)
    cov.stop()

    overall_cov = cov.html_report(directory='htmlcov_all')
    engine_cov = cov.html_report(directory='htmlcov_engine', include=['engine/*'])
    game_cov = cov.html_report(directory='htmlcov_game', include=['game/*'])

    f = open('last_coverage', 'w')
    f.writelines([
        "Overall: {}\n".format(overall_cov),
        "Engine: {}\n".format(engine_cov),
        "Game: {}\n".format(game_cov)
    ])
    f.close()
