from Variable import *
from Grammar import *
from database import *

S = Symbol('S')
A = Symbol('A')
B = Symbol('B')
a = Symbol('a', True)
b = Symbol('b', True)
epsilon = Symbol(is_terminal=True)

symbols = {S, A, B, a, b, epsilon}
terminals = {a, b, epsilon}
start_symbol = S

S.add_production((A, a, B), (b,))
A.add_production((S,), (epsilon,), (A, B))
B.add_production((b, b, b), (A, S, A))

grammar = Grammar(symbols, terminals, start_symbol)
