#!/usr/bin/env bash

coverage run --branch --source='.' --omit='tests/*','test.py' test.py
RESULT="$?"
if [ "$RESULT" != '0' ];
    then
        exit $RESULT
fi

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
exit 0
