from qiskit_aer import StatevectorSimulator
from qiskit.primitives import StatevectorEstimator
from qiskit import transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer import AerError

# Import from Qiskit Aer noise module
from qiskit_aer.noise import (
    NoiseModel,
    QuantumError,
    ReadoutError,
    depolarizing_error,
    pauli_error,
    thermal_relaxation_error,
)

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime.fake_provider import FakeKyoto

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
        

class NoiseModelBackend(Backend):
    def __init__(self):
        super().__init__()
        # Get the noise model of ibmq_lima

        service = QiskitRuntimeService(
            channel='ibm_quantum',
            instance='ibm-q/open/main',
            token='83c14caea83e768600f9d7646593924e9387e8b6eb6cd97700027cb3e602fc8d300b46781b179594b103ddcabaecfbe8a8b70185eed0e58723a0e8a2b5c544f5'
        )

        backend = service.backend("ibm_brisbane")
        noise_model = NoiseModel.from_backend(backend)

        # try:
        #     # Perform a noise simulation
        #     self.simulator = AerSimulator(noise_model=noise_model, device='GPU', method='statevector')
        # except AerError:
        self.simulator = AerSimulator(noise_model=noise_model, method='statevector')
        print("GPU not available, using CPU instead")
        
    def to_isa(self, ansatz, hamiltonian, optimization_level=3):
        target = self.simulator.target
        pm = generate_preset_pass_manager(target=target, optimization_level=optimization_level)

        ansatz_isa = pm.run(ansatz)
        hamiltonian_isa = hamiltonian.apply_layout(ansatz_isa.layout)
        return ansatz_isa, hamiltonian_isa

    def cost_function(self, params, ansatz, hamiltonian, estimator):
        ansatz = ansatz.assign_parameters(params)
        ansatz.measure_all()
        result = self.simulator.run(ansatz).result()
        counts = result.get_counts(ansatz)
        n = sum(counts.values())
        cost = 0
        for k, v in counts.items():
            state = Statevector.from_label(k)
            cost += v/n * state.expectation_value(hamiltonian)
        return cost


class NoisyEstimatorBackend(Backend):
    def __init__(self):
        super().__init__()
        # Get the noise model of ibmq_lima

        # Run the sampler job locally using FakeManilaV2
        fake_backend = FakeKyoto()
        print(fake_backend.num_qubits)
        # You can use a fixed seed to get fixed results. 
        options = {"simulator": {"seed_simulator": 42}}
        
        # Define Estimator  
        self.simulator = Estimator(backend=fake_backend, options=options)

    def to_isa(self, ansatz, hamiltonian, optimization_level=3):
        backend = FakeKyoto()
        ansatz_isa = transpile(ansatz, backend=backend)
        hamiltonian_isa = hamiltonian.apply_layout(ansatz_isa.layout)
        return ansatz_isa, hamiltonian_isa

    def cost_function(self, params, ansatz, hamiltonian, estimator):
        pub = (ansatz, [hamiltonian], [params])
        result = estimator.run(pubs=[pub]).result()
        cost = result[0].data.evs[0]
        return cost