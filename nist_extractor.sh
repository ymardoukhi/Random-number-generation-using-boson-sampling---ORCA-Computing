#!/bin/bash

# A script that processes the NIST SP800-2 output
# Some of the tests have subtests. Other are a 
# single test. We separate them and use grep to 
# break up thi NIST output file into different 
# files such that those can be further processed 
# by pandas library in python. This helps use 
# to plot them individually for a better visualisation 
# of the data

# Arguments:
# $1 -> number of photons
# $2 -> number of modes
# $3 -> number of parameters
# $4 -> version
# $5 -> protocal could be vonnoumann, huffman and permutation

# create a nist directory if it does not exist
DIR="data/n$1_m$2_nparam$3_v$4"

if ! [ -d "$DIR/nist/$5" ]; then
	mkdir -p $DIR/nist/$5
fi

# list of tests that have single test
TESTS=("Frequency" "Runs" "LongestRun" "Rank" "FFT" "Universal" "ApproximateEntropy", "LinearComplexity")

for TEST in ${TESTS[@]}
do
	grep "^.*${TEST}$" $DIR/nist_$5.txt | awk '{print $(NF) "\t" $11}' >> $DIR/nist/$5/SingleTests.txt
done
sed -i '1s/^/test\tp-value\n/' $DIR/nist/$5/SingleTests.txt

# list of tests that have subtests
TESTS=("CumulativeSums" "NonOverlappingTemplate" "RandomExcursions" "RandomExcursionsVariant")
for TEST in ${TESTS[@]}
do
	grep "^.*${TEST}$" $DIR/nist_$5.txt | awk '{print $(NF) "\t" $11}' > $DIR/nist/$5/$TEST.txt
	sed -i '1s/^/test\tp-value\n/' $DIR/nist/$5/$TEST.txt
done




