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
import pathlib
import json

WORDDICT = {}
for line in sys.stdin:
    term = line.split("\t")[0].lower()
    value = line.split("\t")[1]
    if term.isspace() or not term:
        continue

    temp = str(term) + " " + str(value)
    if temp in WORDDICT:
        WORDDICT[temp] += 1
    else:
        WORDDICT[temp] = 1

SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
""" analysis 1164	4
ancient 1164	2
animal 1164	2
annealing 1164	1
answering 1164	1
antilogic 1164	2 """
# termfreq = {}

idf = {}
for key in SORTEDDICT:
    temp = key.split()
    if temp[0] in idf:
        # termfreq[temp[0]] += SORTEDDICT[key]
        idf[temp[0]] += 1
    else:
        # termfreq[temp[0]] = SORTEDDICT[key]
        idf[temp[0]] = 1

# idf now contains how many docs contain the word

# this is N
total_doc_num = 0


with open("total_document_count.txt", "r") as docc:
    total_doc_num = int(docc.read())
    # print("N is " + str(total_doc_num))

idf = collections.OrderedDict(sorted(idf.items()))

# Get real idf values in dictionary
# print("IDF goes here: ")
for key in idf:
    temp = math.log(total_doc_num / idf[key], 10)
    idf[key] = temp
    # print(key, idf[key])

# print(json.dumps(idf, indent=4))

# OH: 
    # weird csv parsing
    # can we write files and read later
    # how to norm factor


""" dirr = pathlib.Path("input/test_small.csv")
with open(dirr, "r") as fil:
    # For each document:
    # Get doc ID, then loops  through unique terms in doc
    # SUM:  square of ^2 * idf of term ^ 2
    for key in SORTEDDICT:
        temp = math.log(total_doc_num / SORTEDDICT[key], 10)
        SORTEDDICT[key] = temp
        fil.write(key + "\t" + str(SORTEDDICT[key]) + "\n")
        print(key, SORTEDDICT[key]) """

# print("big_dict goes here: ")
big_dict = {}
inverted_dict = {}
for key in SORTEDDICT:
    term = key.split()[0]
    docid = key.split()[1]

    # Build big dict
    if not term in big_dict:
        big_dict[term] = {}

    big_dict[term][docid] = SORTEDDICT[key]
    # Inverted dict

# print(json.dumps(big_dict, indent=4))
# Normalization factors

# print("inverted dict: ")


    # inv_map = {v: k for k, v in dict.items()}

# term    idf    docid_x    doc_id_x_freq    .....
# normalalization factor docid
# LAST part of this reduce func.

for term in big_dict:
    for docid in big_dict[term]:
        print(term, "\t", idf[term], "\t", docid, "\t", big_dict[term][docid])


"""
# ouput of job 1 input of map2
term    idf     717    freq
term    idf     1164   freq

# output of map2
717 term idf freq
1164 term idf freq

# reduce 2 gets the above with same keys
dictionary of docids  """
