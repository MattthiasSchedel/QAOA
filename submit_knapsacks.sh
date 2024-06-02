#!/bin/bash

# generate maxcut problem
min_elements=3
max_elements=10

# sbatch generate_problem.sh $number_of_nodes $number_of_edges --output=generate_maxcut.out
# sh generate_problem.sh $number_of_nodes $number_of_edges
# filename=maxcut_problem_$number_of_nodes\_$number_of_edges.txt
# echo $filename
# test the maxcut problem 
min_number_of_layers=1
max_number_of_layers=30
number_of_repetitions=100

# wait for the problem to be generated
sleep 30

for number_of_layers in $(seq $min_number_of_layers $max_number_of_layers)
do
    for number_of_elements in $(seq $min_elements $max_elements)
    do
        problem_name="knapsack_problem_${number_of_elements}_$.txt"
        echo $problem_name
        sbatch test_problem_optimal.sh "$problem_name" $number_of_layers $number_of_repetitions
    done
done

for number_of_layers in $(seq $min_number_of_layers $max_number_of_layers)
do
    for number_of_elements in $(seq $min_elements $max_elements)
    do
        for i in $(seq 1 $number_of_repetitions)
        do
            problem_name="knapsack_problem_${number_of_elements}_$.txt"
            echo $problem_name
            sbatch test_problem.sh "$problem_name" $number_of_layers $i
        done
    done
done
