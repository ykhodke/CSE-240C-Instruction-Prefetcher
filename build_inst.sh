#!/bin/bash

## This is the list of prefetchers we are testing ##
Prefetchers=('no' 'BIP' 'Barca' 'D_JOLT' 'EIP' 'fnl_mma' 'mana' 'pips' 'tap')

## Building all the prefetchers ##
for i in {0..8}; do 
  printf "Building with prefetcher ${Prefetchers[i]}\n"
  printf "./build_champsim.sh hashed_perceptron <your_l1i_prefetcher_here> next_line spp_dev no lru 1\n"
  ./build_champsim.sh hashed_perceptron ${Prefetchers[i]} next_line spp_dev no lru 1
done