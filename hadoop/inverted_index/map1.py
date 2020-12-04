#!/usr/bin/env python3
"""Map 1."""

# Outline for the whole project:
# Follow this format:
# <term> <idf> <doc_id_x> <occurrences in doc_id_x> <doc_id_x normalization factor before sqrt> <doc_id_y> <occurrences in doc_id_y> <doc_id_y normalization factor before sqrt> ...

import sys
import csv
import re

csv.field_size_limit(sys.maxsize)

for row in csv.reader(sys.stdin):
# for line in sys.stdin:
    doc_id = row[0]
    title_words = row[1].split()
    # print("doc_id is " + doc_id)
    # print("doc_title is " + doc_title)
    content = row[2].split()
    for word in title_words:
        content.append(word)

    # Get stopwords list
    stopwords = []
    with open("stopwords.txt", "r") as docc:
        for line in docc.readlines():
            line = line.lower()
            line = line.rstrip()
            stopwords.append(line)
    # print("N is " + str(total_doc_num))

    for word in content:
        word = re.sub(r'[^a-zA-Z0-9]+', '', word)
        word = word.lower()
        word = word.rstrip()
        if word.isspace() or word in stopwords:
            continue
        print(word + "\t" + doc_id)

