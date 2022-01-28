#!/bin/bash
## This is the list of prefetchers we are testing ##
#Prefetchers=('no' 'BIP' 'barca' 'D_JOLT' 'EIP' 'fnl_mma' 'mana' 'pips' 'taps')
#Prefetchers=('pips_ns_2' 'pips_ns_6' 'pips_ns_8' 'pips_t_2' 'pips_t_5' 'pips_t_9' 'pips_t_11')
Prefetchers=('pips_ns_2' 'pips_t_9' 'pips_hm' 'pips_hm_l')

## Building all the prefetchers ##
for i in {2..3}; do 
  printf "Building with prefetcher ${Prefetchers[i]}\n"
  printf "./build_champsim.sh hashed_perceptron ${Prefetchers[i]} next_line spp_dev no lru 1\n"
  ./build_champsim.sh hashed_perceptron ${Prefetchers[i]} next_line spp_dev no lru 1

  binary="hashed_perceptron-${Prefetchers[i]}-next_line-spp_dev-no-lru-1core"

  #printf "${binary}"

  printf $"\n\n ------------ Running all the traces for ${i#*/} ------------\n\n"
    for j in dpc3_traces/*; do
    printf "\n \t ./run_champsim.sh  ${binary} 50 50 ${j#*/}\n"
    ./run_champsim.sh ${binary} 50 50 ${j#*/} &
  done
  wait
done
