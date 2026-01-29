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


# def grover_oracle_1(circuit, qbits): #01
#     theta = math.pi

#     # équivalent de :
#     # RY(theta/2) -- CX -- RY(-theta/2) -- CX
#     circuit.append(cirq.ry(theta / 2)(qbits[1]))
#     circuit.append(cirq.CNOT(qbits[0], qbits[1]))
#     circuit.append(cirq.ry(-theta / 2)(qbits[1]))
#     circuit.append(cirq.CNOT(qbits[0], qbits[1]))

# def grover_oracle_2(circuit, qbits): #111
#     # équivalent exact de :
#     # H(2) -> CCX(0,1,2) -> H(2)

#     circuit.append(cirq.H(qbits[2]))
#     circuit.append(cirq.CCNOT(qbits[0], qbits[1], qbits[2]))
#     circuit.append(cirq.H(qbits[2]))

# def grover_oracle_3(circuit, qbits): #110
#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))

#     # CZ(1,2)
#     circuit.append(cirq.CZ(qbits[1], qbits[2]))

#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))

# def grover_oracle_4(circuit, qbits): #1111
#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))

#     # CCX(1,3,2)
#     circuit.append(cirq.CCNOT(qbits[1], qbits[3], qbits[2]))

#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))

# def grover_oracle_5(circuit, qbits): #01111 11111
#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))

#     # CCX(1,3,2)
#     circuit.append(cirq.CCNOT(qbits[1], qbits[3], qbits[2]))

#     # CH(0,2)
#     circuit.append(cirq.H(qbits[2]).controlled_by(qbits[0]))


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
