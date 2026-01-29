import math
import signal
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

SHOT = 500


def grover(Y, oracle_fn):
    if Y < 2:
        raise ValueError("Number of qubits must be at least 2.")

    qc = QuantumCircuit(Y, Y)
    for q in range(Y):
        qc.h(q)

    oracle = oracle_fn(Y)
    print(f"Oracle:\n{oracle}")

    diffuser = diffuser_fn(Y)

    iterations = math.floor((math.pi / 4) * math.sqrt(2**Y))
    for _ in range(iterations):
        qc.append(oracle, range(Y))
        qc.compose(diffuser, range(Y), inplace=True)

    qc.measure(list(range(Y)), list(range(Y)))

    print(f"Circuit:\n{qc}")

    simulator = AerSimulator()
    tqc = transpile(qc, simulator)
    job = simulator.run(tqc, shots=SHOT)

    result = job.result()
    counts = result.get_counts()

    plot_histogram(counts, title="Grover")
    plt.show()

    return counts


def grover_oracle(nqubits: int):  # 111
    if nqubits != 3:
        raise ValueError("Number of qubits must be 3 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle")

    oracle.h(nqubits - 1)
    oracle.ccx(0, 1, 2)
    oracle.h(nqubits - 1)

    return oracle


def grover_oracle_1(nqubits: int):  # 01
    if nqubits != 2:
        raise ValueError("Number of qubits must be 2 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle_1")

    theta = math.pi
    oracle.ry(theta / 2, 1)
    oracle.cx(0, 1)
    oracle.ry(-theta / 2, 1)
    oracle.cx(0, 1)

    return oracle


def grover_oracle_2(nqubits: int):  # 111
    if nqubits != 3:
        raise ValueError("Number of qubits must be 3 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle_2")

    oracle.h(2)
    oracle.ccx(0, 1, 2)
    oracle.h(2)

    return oracle


def grover_oracle_3(nqubits: int):  # 110
    if nqubits != 3:
        raise ValueError("Number of qubits must be 3 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle_3")

    oracle.ch(0, 2)
    oracle.cz(1, 2)
    oracle.ch(0, 2)

    return oracle


def grover_oracle_4(nqubits: int):  # 1111
    if nqubits != 4:
        raise ValueError("Number of qubits must be 4 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle_4")

    oracle.ch(0, 2)
    oracle.ccx(1, 3, 2)
    oracle.ch(0, 2)

    return oracle


def grover_oracle_5(nqubits: int):  # 01111 11111
    if nqubits != 5:
        raise ValueError("Number of qubits must be 5 for this oracle.")

    oracle = QuantumCircuit(nqubits, name="oracle_5")

    oracle.ch(0, 2)
    oracle.ccx(1, 3, 2)
    oracle.ch(0, 2)

    return oracle


def diffuser_fn(nqubits: int):
    diffuser = QuantumCircuit(nqubits, name="diffuser")
    controls = list(range(nqubits - 1))
    target = nqubits - 1

    for q in range(nqubits):
        diffuser.h(q)
    for q in range(nqubits):
        diffuser.x(q)

    diffuser.h(target)
    if len(controls) == 0:
        diffuser.z(target)
    elif len(controls) == 1:
        diffuser.cx(controls[0], target)
    elif len(controls) == 2:
        diffuser.ccx(controls[0], controls[1], target)
    else:
        diffuser.mcx(controls, target)
    diffuser.h(target)
    for q in range(nqubits):
        diffuser.x(q)
    for q in range(nqubits):
        diffuser.h(q)

    return diffuser


def main():
    try:
        signal.signal(
            signal.SIGINT,
            lambda *_: (
                print("\033[2Dftl_quantum: CTRL+C sent by user."),
                exit(1),
            ),
        )
        grover(3, grover_oracle)
        grover(2, grover_oracle_1)
        grover(3, grover_oracle_2)
        grover(3, grover_oracle_3)
        grover(4, grover_oracle_4)
        grover(5, grover_oracle_5)
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
