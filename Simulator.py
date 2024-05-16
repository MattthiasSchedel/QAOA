from ProblemGenerator import ProblemGenerator
from threading import Thread

def main():
    generator = ProblemGenerator()
    problem = generator.generate_knapsack(5, (5, 20), (5, 63))
    # call the visualization function in a separate thread to avoid blocking the notebook
    thread = Thread(target=problem.visualize_problem)
    thread.start()
    # print(problem. qubo)
    print(problem.solution)
    problem2 = generator.generate_maxcut(5, 7, weights=True)
    thread2 = Thread(target=problem2.visualize_problem)
    thread2.start()
    print(problem2.solution)

    input("Press any key to exit...")
    thread.join()



if __name__ == "__main__":
    main()