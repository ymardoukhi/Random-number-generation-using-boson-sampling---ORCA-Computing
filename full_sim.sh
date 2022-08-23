#!/bin/bash

# bash script to execute all the necessary 
# simulations to generate binary streams 
# ready to be used with NIST Statistical Test Suit
python main_exact.py $1 $2 $3 $4
python main_sim.py $1 $2 $3 $4 $5
python main_huffman.py $1 $2 $3 $4 $5
python main_permutation.py $1 $2 $3 $4 $5

PROTS=("vonneumann" "huffman" "permutation")

for PROT in ${PROTS[@]}
do
	python binstrs2binstream.py data/n$1_m$2_nparam$3_v$4/$PROT_strs_N$5.json data/n$1_m$2_nparam$3_v$4/$PROT.bin
done
