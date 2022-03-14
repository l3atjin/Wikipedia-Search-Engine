#!/usr/bin/env python3
"""Map example."""

import sys

for line in sys.stdin:
    line.rstrip()
    words = line.split(",")
    source = words[0]
    if source == "source_alum":
        uniqname = words[1]
        dorm = words[2]
        fan = words[3]
        app_rating = words[4]
        print(dorm, "\t1", source, "\t1", uniqname, "\t1", fan, "\t1", app_rating)
    else:
        dorm = words[1]
        pets = words[2]
        dist = words[3]
        noise = words[4]
        print(dorm, "\t1", source, "\t1", pets, "\t1", dist, "\t1", noise)

    
