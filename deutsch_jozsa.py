import cirq
import signal
import matplotlib.pyplot as plt
# import numpy as np

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


# def oracle_balanced_random():
#     b = np.random.randint(1, 2**3)
#     b_str = format(b, '03b')
#     print(f"Balanced oracle with b = {b_str}")

#     def oracle(circuit, inputs, output):
#         for i, bit in enumerate(b_str):
#             if bit == '1':
#                 circuit.append(cirq.X(inputs[i]))

#         for q in inputs:
#             circuit.append(cirq.CNOT(q, output))

#         for i, bit in enumerate(b_str):
#             if bit == '1':
#                 circuit.append(cirq.X(inputs[i]))

#     return oracle

# def oracle_constant_random():
#     """
#     Oracle constant aléatoire pour Deutsch-Jozsa
#     f(x) = 0 ou f(x) = 1
#     """
#     value = np.random.randint(2)
#     print(f"Constant oracle with f(x) = {value}")

#     def oracle(circuit, _, output):
#         if value == 1:
#             circuit.append(cirq.X(output))

#     return oracle


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
        # deutsch_jozsa(oracle_constant_random)
        # oracle = oracle_constant_random()
        deutsch_jozsa(oracle_constant)
        deutsch_jozsa(oracle_balanced)
    except Exception as e:
        print(f"ftl_quantum: An error occurred: {e}")


if __name__ == "__main__":
    main()
