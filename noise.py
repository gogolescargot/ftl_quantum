import signal
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.visualization import plot_histogram


SHOT = 500
NOISE = 0.05

# Pour avoir accès aux vraies machines quantiques il faut un compte IBM Quantum mais il faut enregistrer une carte de credit pour activer ce dernier,
# malheureusement ma carte de credit ne fonctionne pas avec IBM Quantum donc je ne peux pas tester cette partie.
# Donc je fais une simulation avec du bruit pour simuler les erreurs des vraies machines quantiques.


def noise():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    noise_model = NoiseModel()
    single_qubit_err = depolarizing_error(NOISE, 1)
    two_qubit_err = depolarizing_error(NOISE, 2)

    noise_model.add_all_qubit_quantum_error(
        single_qubit_err, ["h", "u1", "u2", "u3", "x", "id"]
    )
    noise_model.add_all_qubit_quantum_error(two_qubit_err, ["cx", "cz"])

    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    job = simulator.run(tqc, shots=SHOT, noise_model=noise_model)

    result = job.result()
    counts = result.get_counts()

    print(f"Circuit:\n{qc}")
    plot_histogram(counts, title=f"Noise p={NOISE}")
    plt.show()


def main():
    try:
        signal.signal(
            signal.SIGINT,
            lambda *_: (
                print("\033[2Dftl_quantum: CTRL+C sent by user."),
                exit(1),
            ),
        )
        noise()
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
