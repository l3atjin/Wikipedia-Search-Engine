#!/bin/bash
#
# Example of how to chain mapreduce jobs together.  The output of one
# job is the input to the next.
#
# Hadoop options
# jar index/hadoop/hadoop-streaming-2.7.2.jar   # Hadoop configuration
# -input <directory>                            # Input directory
# -output <directory>                           # Output directory
# -mapper <exec_name>                           # Mapper executable
# -reducer <exec_name>                          # Reducer executable

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# Remove first output directory, if it exists
rm -rf output1
rm -rf output0
rm -rf output2
rm -rf output3
rm -rf total_document_count.txt

# job0 only counts the num of docs
# jobn-1's output must be jobn's input
# reduce0 should only be run by one worker

# up to 9

# Run first MapReduce job
# Count the number of webpages

# 1. Finish job0
# 2. Make an outline/pseudocode

hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input input \
  -output output0 \
  -mapper ./map0.py \
  -reducer ./reduce0.py \

# Remove second output directory, if it exists

hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input input \
  -output output1 \
  -mapper ./map1.py \
  -reducer ./reduce1.py \

hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input output1 \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py \

hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input output2 \
  -output output3 \
  -mapper ./map3.py \
  -reducer ./reduce3.py \

cat output3/part-00000 output3/part-00001 output3/part-00002 output3/part-00003 > inverted_index.txt

echo before comment
: <<'END'
# Run second MapReduce job

hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input input \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py \



hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input tmp \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py \

hadoop \
  jar hadoop-streaming-2.7.2.jar \
  -input input \
  -output output1 \
  -mapper ./map01.py \
  -reducer ./reduce01.py
END
echo after comment
