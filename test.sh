#!/bin/sh

set -e # exit immediately if newman complains
trap 'kill $PID' EXIT # kill the server on exit

./run.sh &
PID=$! # record the PID

newman run basic_endpoints_testing.postman_collection.json
newman run extensions_testing.postman_collection.json