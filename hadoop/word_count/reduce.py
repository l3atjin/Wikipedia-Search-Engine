#!/usr/bin/env python3
"""Reduce example."""

import sys
import collections

# print(dorm, "\t1", source, "\t1", uniqname, "\t1", fan, "\t1", app_rating)
# print(dorm, "\t1", source, "\t1", pets, "\t1", dist, "\t1", noise)
# <distance_to_ugli>,<noise_level>,<dorm_name>,<average_rating>,<pets_allowed>
# short,quiet,South Quad,0.70,true

WORDDICT = {}
for line in sys.stdin:
    words = line.split("\t")
    dorm = words[0]
    source = words[1]

    if not WORDDICT[dorm]:
        WORDDICT[dorm] = {
            "rating": 0.0,
            "num_rating": 0,
            "distance": 0,
            "noise": "",
            "pets": ""
        }

    if source == "source_alum":
        WORDDICT[dorm]["rating"] += float(words[4])
        WORDDICT[dorm]["num_rating"] += 1
    else:
        WORDDICT[dorm]["noise"] = words[4]
        WORDDICT[dorm]["distance"] = words[3]
        WORDDICT[dorm]["pets"] = words[2]

    

SORTEDDICT = collections.OrderedDict(sorted(WORDDICT.items()))
for key in SORTEDDICT:
    print(key, "\t", SORTEDDICT[key]["distance"], "\t", SORTEDDICT[key]["noise"], "\t", SORTEDDICT[key]["rating"]/SORTEDDICT[key]["num_rating"], "\t", SORTEDDICT[key]["pets"])
