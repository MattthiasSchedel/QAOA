#!/bin/bash

min_nodes=3
max_nodes=9

min_layers=1
max_layers=30

number_of_repetitions=100

max_iterations=(-2 200 400 800 1200)
tolerances=(-2 1e-2 1e-3 1e-4 1e-5 1e-6)

for number_of_nodes in $(seq $min_nodes $max_nodes)
do
    number_of_edges=$((number_of_nodes * (number_of_nodes - 1) / 2))
    problem_name="maxcut_problem_${number_of_nodes}_${number_of_edges}.txt"
    echo $problem_name

    for iterations in "${max_iterations[@]}"
    do 
        for tolerance in "${tolerances[@]}"
        do
            for number_of_layers in $(seq $min_layers $max_layers)
            do
                sbatch test_problem_optimal.sh "$problem_name" $number_of_layers $number_of_repetitions $iterations $tolerance
            done
        done
    done
done
