#!/bin/bash

find data/python-trainingData/pythonFiles/ -type f -name '*.py' -print0 | 
    while IFS= read -r -d $'\0' filename; do 
        iconv -f utf-8 -t utf-8 -c "$filename" > "$filename".iconv_cleaned_utf8
        mv "$filename".iconv_cleaned_utf8 "$filename"
    done