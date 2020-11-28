#!/usr/bin/env python3
"""Reduce 1."""

# Outline
# This is the reducer exec for counting the total num of docs in input.csv

# Important: https://piazza.com/class/k9vihaw2wd07b0?cid=3229

# Use hadoop to create Inverted Index from input.csv
# Follow this format:
# <term> <idf> <doc_id_x> <occurrences in doc_id_x> <doc_id_x normalization factor before sqrt> <doc_id_y> <occurrences in doc_id_y> <doc_id_y normalization factor before sqrt> ...

import sys
import collections

WORDDICT = {}
for line in sys.stdin:
    word = line.split("\t")[0]
    if word in WORDDICT:
        WORDDICT[word] += 1
    else:
        WORDDICT[word] = 1

SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
for key in SORTEDDICT:
    print(key, SORTEDDICT[key])
