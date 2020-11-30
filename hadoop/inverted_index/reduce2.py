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
import math

WORDDICT = {}
for line in sys.stdin:
    term = line.split("\t")[0].rstrip()
    value = line.split("\t")[1].rstrip()

    docid = value.split()[0].rstrip()
    freq = value.split()[1].rstrip()

    if term in WORDDICT:
        WORDDICT[term][docid] = freq
    else:
        WORDDICT[term] = {}
        WORDDICT[term][docid] = freq

direc = pathlib.Path("tmp/inverted_index.txt")

idf = {}

with open("idf.txt", "r") as fil:
    # Writing data to a file
    for line in fil:
        term = line.split()[0].rstrip()
        value = line.split()[1].rstrip()
        idf[term] = value

SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))

direc = pathlib.Path("tmp/inverted_index.txt")
with open(direc, "a") as fil:
    # Writing data to a file
    for key in SORTEDDICT:
        fil.write(key.rstrip() + "\t" + str(idf[key.rstrip()]) + "\t" + str(SORTEDDICT[key]) + "\n")

SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
for key in SORTEDDICT:
    print(key, SORTEDDICT[key])

