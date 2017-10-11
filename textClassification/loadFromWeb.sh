#!/usr/bin/env bash

links -dump $1 | tr 'ñ' 'n' | tr -sc 'A-Za-z' '\n' | tr 'A-Z' 'a-z' | sort | uniq -c