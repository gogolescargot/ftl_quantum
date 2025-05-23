# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ggalon <ggalon@student.42lyon.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/05/09 15:20:26 by ggalon            #+#    #+#              #
#    Updated: 2025/05/23 16:09:27 by ggalon           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import cirq
import math
import matplotlib.pyplot as plt

SHOT = 500
NOISE = 0.02

def superposition():
	qubit = cirq.GridQubit(0, 0)

	circuit = cirq.Circuit(
		cirq.H(qubit),
		cirq.measure(qubit)
	)

	print("Circuit: ")
	print(circuit)

	simulator = cirq.Simulator()
	result = simulator.run(circuit, repetitions=SHOT)

	cirq.plot_state_histogram(result)
	plt.show()


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

def noise():
	q0, q1 = cirq.LineQubit.range(2)

	circuit = cirq.Circuit(
		cirq.H(q0),
		cirq.CNOT(q0, q1),
		cirq.measure(q0),
		cirq.measure(q1),
	)

	noisy = circuit.with_noise(cirq.depolarize(p=NOISE))

	print("Circuit: ")
	print(circuit)

	simulator = cirq.Simulator()
	result = simulator.run(noisy, repetitions=SHOT)

	cirq.plot_state_histogram(result, tick_label=["00", "01", "10", "11"])
	plt.show()

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

	cirq.plot_state_histogram(result, tick_label=["000", "001", "010", "011", "100", "101", "110", "111"])
	plt.show()

def oracle_constant(circuit, _, output):
	circuit.append(cirq.X(output))

def oracle_balanced(circuit, input, output):
	circuit.append(cirq.X.on_each(input))
	circuit.append(cirq.CNOT(input[0], output))
	circuit.append(cirq.CNOT(input[1], output))
	circuit.append(cirq.CNOT(input[2], output))
	circuit.append(cirq.X.on_each(input))

def grover(Y, oracle):
	qbits = cirq.LineQubit.range(Y)
	
	circuit = cirq.Circuit()

	circuit.append(cirq.H.on_each(*qbits))

	num_iterations = math.floor((math.pi / 4) * Y)

	for _ in range(num_iterations):
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
	# superposition()
	# entanglement()
	# noise()
	# deutsch_jozsa(oracle_constant)
	# deutsch_jozsa(oracle_balanced)
	grover(3, grover_oracle)

if __name__ == "__main__":
	main()