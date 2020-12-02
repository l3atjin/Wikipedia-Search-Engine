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
import json

WORDDICT = {}
for line in sys.stdin:
    words = line.split("\t")
    term = words[0].rstrip()
    idf = words[1].rstrip()
    docid = words[2].rstrip()
    norm = words[3].rstrip()
    freq = words[4].rstrip()

    if term in WORDDICT:
        WORDDICT[term]["docs"].append({"docid": docid, "norm": norm, "freq": freq})
    else:
        WORDDICT[term] = {}
        WORDDICT[term]["idf"] = idf
        WORDDICT[term]["docs"] = []
        WORDDICT[term]["docs"].append({"docid": docid, "norm": norm, "freq": freq})

WORDDICT = collections.OrderedDict(sorted(WORDDICT.items()))

for term in WORDDICT:
    print(term, "\t", WORDDICT[term]["idf"], "\t", end = '')
    for doc in WORDDICT[term]["docs"]:
        print(doc["docid"], "\t", doc["freq"], "\t", doc["norm"], "\t", end = '')
    print("\n", end = '')

# print(json.dumps(WORDDICT, indent=4))
