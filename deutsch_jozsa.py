import cirq
import signal
import matplotlib.pyplot as plt

SHOT = 500


def deutsch_jozsa(oracle):
    q0, q1, q2, q3 = cirq.LineQubit.range(4)

    circuit = cirq.Circuit()

    circuit.append(cirq.X(q3))
    circuit.append(cirq.H.on_each(q0, q1, q2, q3))
    oracle(circuit, (q0, q1, q2), q3)
    circuit.append(cirq.H.on_each(q0, q1, q2))
    circuit.append(cirq.measure(q0, q1, q2))

    print("Circuit: ")
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=SHOT)

    cirq.plot_state_histogram(
        result,
        tick_label=["000", "001", "010", "011", "100", "101", "110", "111"],
    )
    plt.show()


def oracle_constant(circuit, _, output):
    circuit.append(cirq.X(output))


def oracle_balanced(circuit, input, output):
    circuit.append(cirq.X.on_each(input))
    circuit.append(cirq.CNOT(input[0], output))
    circuit.append(cirq.CNOT(input[1], output))
    circuit.append(cirq.CNOT(input[2], output))
    circuit.append(cirq.X.on_each(input))


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
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
