#!/usr/bin/env bash

cat $1 | sed -e 's/ñ/n/g' | sed -e 's/á/a/g' | sed -e 's/é/e/g' | sed -e 's/í/i/g' | sed -e 's/ó/o/g' | sed -e 's/ú/u/g' | tr -sc 'A-Za-z' '\n' | tr 'A-Z' 'a-z' | sort | uniq -c