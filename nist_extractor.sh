#!/bin/bash

DIR="data/n$1_m$2_nparam$3_v$4"

if ! [ -d "$DIR/nist/$5" ]; then
	mkdir -p $DIR/nist/$5
fi

TESTS=("Frequency" "Runs" "LongestRun" "Rank" "FFT" "Universal" "ApproximateEntropy", "LinearComplexity")

for TEST in ${TESTS[@]}
do
	grep "^.*${TEST}$" $DIR/nist_$5.txt | awk '{print $(NF) "\t" $11}' >> $DIR/nist/$5/SingleTests.txt
done

TESTS=("CumulativeSums" "NonOverlappingTemplate" "RandomExcursions" "RandomExcursionsVariant")
for TEST in ${TESTS[@]}
do
	grep "^.*${TEST}$" $DIR/nist_$5.txt | awk '{print $(NF) "\t" $11}' > $DIR/nist/$5/$TEST.txt
done




