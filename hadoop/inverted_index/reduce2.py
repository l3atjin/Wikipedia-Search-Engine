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
big_dict = {}
for line in sys.stdin:
    words = line.split("\t")
    docid = words[0].rstrip()
    term = words[1].rstrip()
    idf = words[2].rstrip()
    freq = words[3].rstrip()

    if docid in WORDDICT:
        WORDDICT[docid][term] = [idf, freq]
    else:
        WORDDICT[docid] = {}
        WORDDICT[docid][term] = [idf, freq]

    if not term in big_dict:
        big_dict[term] = {}

    big_dict[term] = {
        "docid": docid,
        "freq": freq,
        "idf": idf,
    }


WORDDICT = collections.OrderedDict(sorted(WORDDICT.items()))

norm_fact = {}

for docid in WORDDICT:
    norm_sum = 0
    for term in WORDDICT[docid]:
        norm_sum += math.pow(float(WORDDICT[docid][term][1]), 2) * math.pow(float(WORDDICT[docid][term][0]), 2)
    norm_fact[docid] = norm_sum

for term in big_dict:
    print(term, "\t", big_dict[term]["idf"], "\t", big_dict[term]["docid"], "\t", norm_fact[big_dict[term]["docid"]], "\t", big_dict[term]["freq"])

# print(json.dumps(WORDDICT, indent=4))

