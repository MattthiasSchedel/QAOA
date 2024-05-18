from ProblemGenerator import ProblemGenerator
from QuantumOptimizer import QuantumOptimizer
from Backend import *
import os
import json

def main():
    file_name = "solutions.json"
    problem_file = "problem.txt"
    problem_generator = ProblemGenerator()
    optimizer = QuantumOptimizer()
    backend = StatevectorSimulatorBackend()
    problem = generator.generate_maxcut(5, 7, weights=True)

    solutions = {}
    for i in range(1,30):
        problem.to_qaoa_ansatz(p=i)
        print(f"p={i}")
        for j in range(100):
            optimizer.set_problem(problem)
            optimizer.set_optimizer("L-BFGS-B")
            optimizer.set_backend(backend)
            solution = optimizer.optimize()
            print(f"p = {i}, iteration = {j}, solution = {solution}")
            solutions[f"p={i}, iteration={j}"] = {'solution': solution, 'optimizer': optimizer.to_json()} 

    with open(file_name, "w") as f:
        json.dump(solutions, f)
    
    with open(problem_file, "w") as f:
        f.write(problem.to_json())

if __name__ == "__main__":
    main()