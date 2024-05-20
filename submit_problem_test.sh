#!/bin/bash

# generate maxcut problem
number_of_nodes=10
number_of_edges=20

# sbatch generate_problem.sh $number_of_nodes $number_of_edges --output=generate_maxcut.out
# sh generate_problem.sh $number_of_nodes $number_of_edges
filename=maxcut_problem_$number_of_nodes\_$number_of_edges.txt
echo $filename
# test the maxcut problem 
min_number_of_layers=1
max_number_of_layers=30
number_of_repetitions=100

# wait for the problem to be generated
# sleep 30

for number_of_layers in $(seq $min_number_of_layers $max_number_of_layers)
do
    for i in $(seq 0 $number_of_repetitions)
    do
        sbatch test_problem_noisy.sh $filename $number_of_layers $i --output="qaoa_test$number_of_layers.out"
    done
    sleep 1
    # sbatch test_problem_optimal.sh $filename $number_of_layers $number_of_repetitions --output=qaoa_test$number_of_layers.out
    # sleep 1
    # sh test_problem.sh $filename $number_of_layers $number_of_repetitions
done
