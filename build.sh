#!/bin/sh

if [ ! -d "sparsepp" ]; then
	git clone https://github.com/greg7mdp/sparsepp
fi
g++ -O3 -std=c++11 -lgmpxx -lgmp -I./sparsepp-master discrete.cpp -o discrete
python hash.py
