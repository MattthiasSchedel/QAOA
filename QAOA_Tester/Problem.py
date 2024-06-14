from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.circuit.library import QAOAAnsatz
import networkx as nx
import warnings

# Suppress specific RuntimeWarnings from numpy
warnings.filterwarnings("ignore", message="divide by zero encountered in det")
warnings.filterwarnings("ignore", message="invalid value encountered in det")

class Problem:
    def __init__(self, description):
        self.description = description
        self.qubo = None
        self.quadratic_program = None
        self.solution = None
        self.hamiltonian = None
        self.problem = None
        self.qaoa_ansatz = None
        self.offset = None

    def visualize_problem(self):
        raise NotImplementedError

    def visualize_solution(self):
        raise NotImplementedError

    def to_qubo(self):
        if self.quadratic_program is None:
            raise ValueError("Quadratic program not initialized")
        converter = QuadraticProgramToQubo()
        self.qubo = converter.convert(self.quadratic_program)
        return self.qubo

    def to_quadratic_program(self):
        if self.problem is None:
            raise ValueError("Problem not initialized")
        self.quadratic_program = self.problem.to_quadratic_program()
        return self.quadratic_program

    def to_qaoa_ansatz(self, p):
        if self.qubo is None:
            raise ValueError("Qubo not initialized")
        self.hamiltonian, self.offset = self.qubo.to_ising()
        self.qaoa_ansatz = QAOAAnsatz(self.hamiltonian, p)
        return self.qaoa_ansatz

    def solve(self):
        solutions = []
        # Solve the problem by testing all possible solutions
        length = self.quadratic_program.get_num_binary_vars()
        solution_strings = [f'{i:0{length}b}' for i in range(2**length)]
        for solution_string in solution_strings:
            solution = [int(bit) for bit in solution_string]
            value = self.quadratic_program.objective.evaluate(solution)
            if self.quadratic_program.is_feasible(solution):
                solutions.append((solution, value))
        # print(solution_strings)
        self.solution = max(solutions, key=lambda x: x[1])
        return self.solution

    def solve_qubo(self):
        solutions = []
        # Solve the problem by testing all possible solutions
        length = self.qubo.get_num_binary_vars()
        solution_strings = [f'{i:0{length}b}' for i in range(2**length)]
        for solution_string in solution_strings:
            solution = [int(bit) for bit in solution_string]
            value = self.qubo.objective.evaluate(solution)
            if self.qubo.is_feasible(solution):
                solutions.append((solution, value))
        # print(solution_strings)
        self.solution_qubo = min(solutions, key=lambda x: x[1])
        return self.solution_qubo

    # TODO: not used anymore. Remove?
    def to_json(self):
        return{
            'description': self.description,
            'solution': self.solution
        }
