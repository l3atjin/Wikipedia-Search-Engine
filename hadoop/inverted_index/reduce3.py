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
    line = line.rstrip()
    words = line.split("\t")
    term = words[0].rstrip()
    idf = words[1].rstrip()

    num = 2
    while num < len(words): 
        docid = words[num].rstrip()
        norm = words[num + 1].rstrip()
        freq = words[num + 2].rstrip()

        if term in WORDDICT:
            WORDDICT[term]["docs"].append({"docid": docid, "norm": norm, "freq": freq})
        else:
            WORDDICT[term] = {}
            WORDDICT[term]["idf"] = idf
            WORDDICT[term]["docs"] = []
            WORDDICT[term]["docs"].append({"docid": docid, "norm": norm, "freq": freq})
        num += 3
WORDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
# print("length of big dict:  ", len(WORDDICT))
for term in WORDDICT:
    print(term, "\t", WORDDICT[term]["idf"], "\t", end = '')
    for doc in WORDDICT[term]["docs"]:
        print(doc["docid"], "\t", doc["freq"], "\t", doc["norm"], "\t", end = '')
    print("\n", end = '')

# print(json.dumps(WORDDICT, indent=4))
