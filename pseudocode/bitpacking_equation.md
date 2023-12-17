
# Bit-Packing Equation

Given a sequence of binary digits \( b_1, b_2, \ldots, b_n \) where \( b_1 \) is the least significant bit and \( b_n \) is the most significant bit, the packed integer value \( P \) can be calculated as:

\[ P = \sum_{i=1}^{n} b_i 	imes 2^{(n-i)} \]

Here, each bit \( b_i \) is multiplied by \( 2^{(n-i)} \) to shift it to its correct position in the binary representation of the integer.
