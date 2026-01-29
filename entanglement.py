import cirq
import signal
import matplotlib.pyplot as plt

SHOT = 500


def entanglement():
    q0, q1 = cirq.LineQubit.range(2)

    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0),
        cirq.measure(q1),
    )
    print("Circuit: ")
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=SHOT)

    cirq.plot_state_histogram(result, tick_label=["00", "01", "10", "11"])
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
        entanglement()
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
