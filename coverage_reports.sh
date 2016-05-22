#!/usr/bin/env bash

coverage run --source='.' --omit='tests/*','test.py' test.py

echo ''
echo 'Overall Coverage Report'
coverage report

echo ''
echo 'Engine Coverage Report'
coverage report --include='engine/*'

echo ''
echo 'Game Coverage Report'
coverage report --include='game/*'

coverage html
coverage html --include='engine/*'
coverage html --include='game/*'
