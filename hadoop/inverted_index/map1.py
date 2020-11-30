#!/usr/bin/env python3
"""Map 1."""

# Outline for the whole project:

# Three parts:
#   - Inverted Index(mapreduce) 1
#   - Index server(rest api) 2
#   - Search interface(serverside dynamic page) 3

# Outline
# This is the mapper exec for counting the total num of docs in input.csv

# Use hadoop to create Inverted Index from input.csv

# Hint: remember all key/value pairs with the same key
# will be sent to the same reducer.

# Hint: manually create small test case

# Follow this format:
# <term> <idf> <doc_id_x> <occurrences in doc_id_x> <doc_id_x normalization factor before sqrt> <doc_id_y> <occurrences in doc_id_y> <doc_id_y normalization factor before sqrt> ...

import sys
import csv
import re

for line in sys.stdin:
    # print("Printing line")
    # print(line)
    # print("#########################################################")
    words = line.split()
    header = words[0].split(",")
    doc_id = header[0]
    doc_title = header[1]
    doc_title = re.sub(r'[^a-zA-Z0-9]+', '', doc_title)
    # print("doc_id is " + doc_id)
    # print("doc_title is " + doc_title)
    words.append(doc_title)
    words.pop(0)
    for word in words:
        if word.isspace():
            continue
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)
        word = word.lower()
        print(word + "\t" + doc_id)

