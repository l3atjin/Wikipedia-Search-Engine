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
for key in idf:
    temp = math.log(total_doc_num / idf[key], 10)
    idf[key] = temp

# OH: Is it okay to access this file when it's not piped
# Complexity
# some words are mashed together - csv line what does it do
# how to properly pipe

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
    if not docid in inverted_dict:
        inverted_dict[docid] = {}

    inverted_dict[docid][term] = SORTEDDICT[key]
    
# Normalization factors
norm_fact = {}
for docid in inverted_dict:
    norm_sum = 0
    for term in inverted_dict[docid]:
        norm_sum += math.pow(inverted_dict[docid][term], 2) * math.pow(idf[term], 2)
    
    norm_fact[docid] = norm_sum
    # inv_map = {v: k for k, v in dict.items()}

# term    idf    docid_x    doc_id_x_freq    .....
# normalalization factor docid
# LAST part of this reduce func.

for term in big_dict:
    print(term + "\t", end = '')
    print(idf[term], "\t", end = '')
    for docid in big_dict[term]:
        print(docid, "\t", big_dict[term][docid], "\t", norm_fact[docid])


""" for docid in dict:
    for term in dict[docid]:
        sum += idf[term]^2 * big_dict[term][docid]^2

Objective:
build the dicts:
    big_dict, (close)
    idf, (done)
    normal_factor (tricky because we need to loop through each docid not term)
    with open() """


