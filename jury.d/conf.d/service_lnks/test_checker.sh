#!/bin/bash

# random uuid
FLAG_ID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)
FLAG=$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 8 | head -n 1)
FLAG=$FLAG-$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 4 | head -n 1)
FLAG=$FLAG-$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 4 | head -n 1)
FLAG=$FLAG-$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 4 | head -n 1)
FLAG=$FLAG-$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 12 | head -n 1)

./checker.py "$1" "put" $FLAG_ID $FLAG
sleep 1s
./checker.py "$1" "check" $FLAG_ID $FLAG
