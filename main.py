from Variable import *
from Grammar import *

S = Symbol('S')
A = Symbol('A')
B = Symbol('B')
a = Symbol('a', True)
b = Symbol('b', True)
epsilon = Symbol(is_terminal=True)

symbols = {S, A, B, a, b, epsilon}
terminals = {a, b, epsilon}
start_symbol = S

S.add_production((A, B))
A.add_production((a, A, A), (epsilon,))
B.add_production((b, B, B), (epsilon,))

grammar = Grammar(symbols, terminals, start_symbol)
