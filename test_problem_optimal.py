from QAOA_Tester import ProblemGenerator, QuantumOptimizer, StatevectorEstimatorBackend

import argparse
import array
import pandas as pd
import time
import os

def test_problem(data: dict, layers: int, rep: int, max_iter: int, tol: float):
    problem = ProblemGenerator.from_dict(data)
    problem.to_qaoa_ansatz(layers)
    backend = StatevectorEstimatorBackend()
    optimizer = QuantumOptimizer(maxiter=max_iter)
    optimizer.set_problem(problem)
    optimizer.set_backend(backend)
    optimizer.set_tol(tol)
    
    # create a dataframe to store the result and a general description of the problem
    results = pd.DataFrame()
    results['problem'] = [problem.to_dict()]
    results['layers'] = layers
    results['optimizer'] = [optimizer.to_dict()]

    solutions = []
    parameters = []
    times = []
    for i in range(rep):
        print(f"Rep {i}")
        start = time.time()
        solution = optimizer.optimize()
        end = time.time()
        times.append(end - start)
        solutions.append(solution)
        parameters.append(optimizer.x0)
    print("Done!")
    results['solutions'] = [solutions]
    results['parameters'] = [parameters]
    results['time'] = [times]
    
    # create the folder if it does not exist
    if max_iter is None:
        max_iter = "None"
    if tol is None:
        tol = "None"
    
    foldername = f"results_{problem.name}_{problem.n}_{max_iter}i_{tol}/optimal"
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # save the results to a csv file
    filename = f"{foldername}/results_optimal_{layers}_{rep}.csv"
    results.to_csv(filename)
    print(f"Results saved to {filename}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Print the QUBO of a problem')
    parser.add_argument('filename', type=str, help='Filename of the problem')
    parser.add_argument('layers', type=int, help='Number of QAOA layers')
    parser.add_argument('rep', type=int, help='Number of repetitions')
    # make maxiter and tol optional 
    parser.add_argument('--max_iter', type=int, default=None, help='Number of iterations for optimizer')
    parser.add_argument('--tol', type=float, default=None, help='Tolerance for optimizer')
    args = parser.parse_args()
    # turn the data into a dictionary
    data = None
    with open(args.filename, "r") as f:
        data = eval(f.read())
    # print(data)
    data = eval(f"{data}")

    if args.max_iter == -2:
        args.max_iter = None
    if args.tol == -2:
        args.tol = None

    test_problem(data, args.layers, args.rep, args.max_iter, args.tol)