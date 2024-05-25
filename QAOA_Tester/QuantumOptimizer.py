from scipy.optimize import minimize
import numpy as np
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


class ParameterStrategy:
    RANDOM = 'RANDOM'
    ZEROS = 'ZEROS'
    ONES = 'ONES'

class QuantumOptimizer:
    def __init__(self, optimizer: str = 'COBYLA', maxiter: int = 100, shots: int = 1024, parameter_strategy: ParameterStrategy = ParameterStrategy.RANDOM):
        self.optimizer = optimizer
        self.maxiter = maxiter
        self.tol = None 
        self.backend = None
        self.problem = None
        self.shots = shots
        self.parameter_strategy = parameter_strategy
        self.x0 = None
        self.ansatz_isa = None
        self.hamiltonian_isa = None
        self.cost_function = None
        self.num_iterations_needed = None

    def set_backend(self, backend):
        self.backend = backend
    
    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    def set_problem(self, problem):
        self.problem = problem

    def set_maxiter(self, maxiter):
        self.maxiter = maxiter

    def set_tol(self, tol):
        self.tol = tol

    def set_shots(self, shots):
        self.shots = shots

    def set_parameter_strategy(self, parameter_strategy: ParameterStrategy):
        self.parameter_strategy = parameter_strategy

    def initialize(self):
        if self.problem is None:
            raise ValueError("Problem not set")
        if self.backend is None:
            raise ValueError("Backend not set")
            
        self.ansatz_isa, self.hamiltonian_isa = self.backend.to_isa(self.problem.qaoa_ansatz, self.problem.hamiltonian)
        num_parameters = self.ansatz_isa.num_parameters

        if self.parameter_strategy == ParameterStrategy.RANDOM:
            self.x0 = 2 * np.pi * np.random.rand(num_parameters)
        elif self.parameter_strategy == ParameterStrategy.ZEROS:
            self.x0 = np.zeros(num_parameters)
        elif self.parameter_strategy == ParameterStrategy.ONES:
            self.x0 = np.ones(num_parameters)
        else:
            raise ValueError("Invalid parameter strategy.")
        # return self.x0

        options = {}
        if self.tol is not None:
            options['tol'] = self.tol
        if self.maxiter is not None:
            options['maxiter'] = self.maxiter
        return options


    def optimize(self):
        options = self.initialize()
        
        output = minimize(self.backend.cost_function, self.x0, args=(self.ansatz_isa, self.hamiltonian_isa, self.backend.simulator), method=self.optimizer, options=options)
        self.x0 = output.x
        circuit = self.problem.qaoa_ansatz.assign_parameters(output.x)
        circuit.measure_all()
        # circuit = circuit.decompose()
        result = self.backend.run(circuit)
        # return a list of all results with the highest count
        solution = max(result.get_counts(), key=result.get_counts().get)
        number_of_binary_vars = self.problem.quadratic_program.get_num_binary_vars()
        solution = [int(bit) for bit in solution]
        # if self.problem.quadratic_program.is_feasible(solution):
        #     value = self.problem.quadratic_program.objective.evaluate(solution)
        # else:
        #     value = 0

        value = self.problem.qubo.objective.evaluate(solution)
        return solution, value

    def to_json(self):
        raise DeprecationWarning("This method is deprecated. Use to_dict instead.")
        return {
            'optimizer': self.optimizer,
            'maxiter': self.maxiter,
            'shots': self.shots,
            'parameter_strategy': self.parameter_strategy, 
            'x0': self.x0.tolist() if self.x0 is not None else None,
            'ansatz_isa': str(self.ansatz_isa) if self.ansatz_isa is not None else None,
            'hamiltonian_isa': str(self.hamiltonian_isa) if self.hamiltonian_isa is not None else None,
            'problem': self.problem.to_json() if self.problem is not None else None,
            'backend': self.backend.to_json() if self.backend is not None else None
        }

    def to_dict(self):
        return {
            'optimizer': self.optimizer,
            'maxiter': self.maxiter,
            'shots': self.shots,
            'parameter_strategy': self.parameter_strategy, 
            'x0': self.x0.tolist() if self.x0 is not None else None,
            'backend': self.backend if self.backend is not None else None

        }
        
    
        