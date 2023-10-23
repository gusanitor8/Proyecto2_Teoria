from Variable import *
from Grammar import *
from database import *
from cyk import *
from graphviz import Digraph

E = Symbol('E')
X = Symbol('X')
T = Symbol('T')
Y = Symbol('Y')
F = Symbol('F')
id = Symbol('id', is_terminal=True)
l_parenthesis = Symbol('(', is_terminal=True)
r_parenthesis = Symbol(')', is_terminal=True)
plus = Symbol('+', is_terminal=True)
times = Symbol('*', is_terminal=True)
epsilon = Symbol(is_terminal=True)
# epsilon = Symbol(is_terminal=True)

symbols = {E, X, T, Y, F, id, l_parenthesis, r_parenthesis, plus, times, epsilon}
terminals = {id, l_parenthesis, r_parenthesis, plus, times, epsilon}
start_symbol = E

E.add_production((T, X))
X.add_production((plus, T, X), (epsilon,))
T.add_production((F, Y))
Y.add_production((times, F, Y), (epsilon,))
F.add_production((l_parenthesis, E, r_parenthesis), (id,))


grammar = Grammar(symbols, terminals, start_symbol)
grammar.normalize()

print("diccionario: \n")
dictionary = grammar.to_dict()

# cadenas a testear NO validas
# w = "id + * id" 
# w = "id + id +"
# w = "(id + id"

# cadenas a testear validas
w = "id + id * id"
# w = "id"
# w = "* id"

# Realiza el análisis CYK
output, parse_tree, execution_time = parse_sentence_cyk(w, dictionary)

# Verifica si la cadena pertenece a la gramática
if output:
    print(f"La cadena de entrada '{w}' si pertenece a la gramatica :)")
    print("-----------------------------------------------------------")
    print(f"Tiempo tardado: {execution_time:.6f} segundos")
    # Si deseas visualizar el árbol de análisis, descomenta la siguiente línea:
    visualize_parse_tree(parse_tree)
else:
    print(f"La cadena de entrada '{w}' no pertenece a la gramatica :(")
    print("-----------------------------------------------------------")
    print(f"Tiempo tardado: {execution_time:.6f} segundos")