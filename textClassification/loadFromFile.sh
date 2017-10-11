#!/usr/bin/env bash

cat $1 | tr 'ñ' 'n' | tr -sc 'A-Za-z' '\n' | tr 'A-Z' 'a-z' | sort | uniq -c