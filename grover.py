import cirq
import math
import signal
import matplotlib.pyplot as plt

SHOT = 500


def grover(Y, oracle):
    if Y < 2:
        raise ValueError("Number of qubits must be at least 2.")

    qbits = cirq.LineQubit.range(Y)

    circuit = cirq.Circuit()

    circuit.append(cirq.H.on_each(*qbits))

    for _ in range(math.floor((math.pi / 4) * math.sqrt(2**Y))):
        oracle(circuit, qbits)
        diffuser(circuit, qbits)

    circuit.append(cirq.measure(*qbits))

    print("Circuit:")
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=SHOT)

    cirq.plot_state_histogram(result)
    plt.show()


def grover_oracle(circuit, qbits):
    circuit.append(cirq.H(qbits[-1]))
    circuit.append(cirq.CCNOT(qbits[0], qbits[1], qbits[2]))
    circuit.append(cirq.H(qbits[-1]))


def diffuser(circuit, qbits):
    circuit.append(cirq.H.on_each(*qbits))
    circuit.append(cirq.X.on_each(*qbits))
    circuit.append(cirq.Z(qbits[-1]).controlled_by(*qbits[:-1]))
    circuit.append(cirq.X.on_each(*qbits))
    circuit.append(cirq.H.on_each(*qbits))


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
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
