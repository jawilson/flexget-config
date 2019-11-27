#!/bin/bash
torrentid=$1
torrentname=$2
torrentpath=$3

/usr/bin/curl -X POST http://localhost:5050/api/tasks/execute/ -H 'Authorization: Token aeba2402c3894f8ecfcde9b239ab381d234798133717150892cfbaa8' -H 'Content-Type: application/json' -d '{"tasks":["Series-Decompress", "Movies-Decompress"]}'
