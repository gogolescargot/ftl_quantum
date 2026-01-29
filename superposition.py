import cirq
import signal
import matplotlib.pyplot as plt

SHOT = 500


def superposition():
    qubit = cirq.GridQubit(0, 0)

    circuit = cirq.Circuit(cirq.H(qubit), cirq.measure(qubit))

    print("Circuit: ")
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=SHOT)

    cirq.plot_state_histogram(result)
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
        superposition()
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
