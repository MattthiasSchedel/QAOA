from QAOA_Tester import ProblemGenerator
import argparse

def generate_knapsack(num_nodes: int, num_edges: int, weights=False):
    problem_generator = ProblemGenerator()
    problem = problem_generator.generate_knapsack(num_nodes, num_edges, weights=weights)
    return problem

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a Knapsack problem')
    parser.add_argument('num_nodes', type=int, help='Number of nodes in the graph')
    parser.add_argument('num_edges', type=int, help='Number of edges in the graph')
    parser.add_argument('--weights', action='store_true', help='Generate a weighted graph')
    args = parser.parse_args()
    # num nodes is argument or 7
    num_nodes = args.num_nodes if args.num_nodes else 5
    num_edges = args.num_edges if args.num_edges else 7
    weights = args.weights if args.weights else True
    
    problem = generate_knapsack(num_nodes, num_edges, weights)
    filename = f"maxcut_problem_{num_nodes}_{num_edges}.txt"
    with open(filename, "w") as f:
        f.write(f"{problem.to_dict()}")