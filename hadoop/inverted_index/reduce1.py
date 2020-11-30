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

WORDDICT = {}
for line in sys.stdin:
    term = line.split("\t")[0].lower()
    value = line.split("\t")[1]
    if term.isspace() or not term:
        continue

    temp = str(term) + " " + str(value)
    print("temp is " + temp)
    if temp in WORDDICT:
        WORDDICT[temp] += 1
    else:
        WORDDICT[temp] = 1

direc = pathlib.Path("tmp/term_freq.txt")
SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
with open(direc, "a") as fil:
    # Writing data to a file
    for key in SORTEDDICT:
        fil.write(key.rstrip() + "\t" + str(SORTEDDICT[key]) + "\n")

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

total_doc_num = 0

""" termfreq = collections.OrderedDict(sorted(termfreq.items()))
with open("term_freq.txt", "a") as fil:
    # Writing data to a file
    for key in termfreq:
        fil.write(key + "\t" + str(termfreq[key]) + "\n") """

with open("total_document_count.txt", "r") as docc:
    total_doc_num = int(docc.read())
    # print("N is " + str(total_doc_num))

SORTEDDICT = collections.OrderedDict(sorted(idf.items()))
with open("idf.txt", "a") as fil:
    # Writing data to a file
    for key in SORTEDDICT:
        temp = math.log(total_doc_num / SORTEDDICT[key], 10)
        SORTEDDICT[key] = temp
        fil.write(key + "\t" + str(SORTEDDICT[key]) + "\n")
        print(key, SORTEDDICT[key])

