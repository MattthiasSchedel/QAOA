from qiskit_aer import StatevectorSimulator
from qiskit.primitives import StatevectorEstimator
from qiskit import transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Statevector



class Backend:
    def __init__(self):
        self.simulator = None

    def to_isa(self, ansatz, hamiltonian, optimization_level=3):
        target = self.simulator.target
        pm = generate_preset_pass_manager(target=target, optimization_level=optimization_level)

        ansatz_isa = pm.run(ansatz)
        hamiltonian_isa = hamiltonian.apply_layout(ansatz_isa.layout)
        return ansatz_isa, hamiltonian_isa

    def cost_function(self, params, ansatz, hamiltonian, estimator):
        raise NotImplementedError

    def run(self, circuit):
        backend = StatevectorSimulator()
        circuit = transpile(circuit, backend)
        return backend.run(circuit).result()

    def to_json(self):
        return {
            'simulator': str(self.simulator),
        }


class StatevectorEstimatorBackend(Backend):
    def __init__(self):
        super().__init__()
        self.simulator = StatevectorEstimator()

    def to_isa(self, ansatz, hamiltonian, optimization_level=3):
        return ansatz, hamiltonian # No need to convert to ISA for the StatevectorEstimator

    def cost_function(self, params, ansatz, hamiltonian, estimator):
        pub = (ansatz, [hamiltonian], [params])
        result = estimator.run(pubs=[pub]).result()
        cost = result[0].data.evs[0]
        return cost


class StatevectorSimulatorBackend(Backend):
    def __init__(self):
        super().__init__()
        self.simulator = StatevectorSimulator()

    def to_isa(self, ansatz, hamiltonian, optimization_level=3):
        target = self.simulator.target
        pm = generate_preset_pass_manager(target=target, optimization_level=optimization_level)

        ansatz_isa = pm.run(ansatz)
        hamiltonian_isa = hamiltonian.apply_layout(ansatz_isa.layout)
        return ansatz_isa, hamiltonian_isa

    def cost_function(self, params, ansatz, hamiltonian, estimator):
        ansatz = ansatz.assign_parameters(params)
        result = self.simulator.run(ansatz).result()
        statevector = result.get_statevector()
        cost = Statevector(statevector).expectation_value(hamiltonian)
        return cost.real
        

    
