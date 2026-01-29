import signal
import matplotlib.pyplot as plt
# import numpy as np

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOT = 500


def deutsch_jozsa(oracle):
    qc = QuantumCircuit(4, 3)
    qc.x(3)
    for q in range(4):
        qc.h(q)

    oracle(qc, 4)

    for q in range(3):
        qc.h(q)
    qc.measure([0, 1, 2], [0, 1, 2])

    sim = AerSimulator()
    tqc = transpile(qc, sim)
    job = sim.run(tqc, shots=SHOT)

    result = job.result()
    counts = result.get_counts()

    print(f"Circuit:\n{qc}")
    plot_histogram(counts, title="Deutsch-Jozsa")
    plt.show()


def oracle_constant(qc: QuantumCircuit, nqubits):
    oracle = QuantumCircuit(nqubits, name="oracle_constant")

    oracle.x(nqubits - 1)

    print(f"Oracle constant:\n{oracle}")
    qc.append(oracle, range(nqubits))


def oracle_balanced(qc: QuantumCircuit, nqubits):
    oracle = QuantumCircuit(nqubits, name="oracle_balanced")

    for i in range(nqubits - 1):
        oracle.x(i)
    for i in range(nqubits - 1):
        oracle.cx(i, nqubits - 1)
    for i in range(nqubits - 1):
        oracle.x(i)

    print(f"Oracle balanced:\n{oracle}")
    qc.append(oracle, range(nqubits))


# def oracle_constant_random(qc: QuantumCircuit, nqubits):
#     oracle = QuantumCircuit(nqubits, name="oracle_constant_random")

#     if np.random.randint(2) == 1:
#         oracle.x(nqubits - 1)
#     print(f"Oracle constant random:\n{oracle}")
#     qc.append(oracle, range(nqubits))


# def oracle_balanced_random(qc: QuantumCircuit, nqubits):
#     oracle = QuantumCircuit(nqubits, name="oracle_balanced_random")

#     b = np.random.randint(1, 2**nqubits - 1)
#     b_str = format(b, "0" + str(nqubits - 1) + "b")
#     for qubit in range(len(b_str)):
#         if b_str[qubit] == "1":
#             oracle.x(qubit)

#     for qubit in range(nqubits - 1):
#         oracle.cx(qubit, nqubits - 1)
#     for qubit in range(len(b_str)):
#         if b_str[qubit] == "1":
#             oracle.x(qubit)

#     print(f"Oracle balanced random (b={b_str}):\n{oracle}")
#     qc.append(oracle, range(nqubits))


def main():
    try:
        signal.signal(
            signal.SIGINT,
            lambda *_: (
                print("\033[2Dftl_quantum: CTRL+C sent by user."),
                exit(1),
            ),
        )
        deutsch_jozsa(oracle_constant)
        deutsch_jozsa(oracle_balanced)
        # deutsch_jozsa(oracle_constant_random)
        # deutsch_jozsa(oracle_balanced_random)
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
