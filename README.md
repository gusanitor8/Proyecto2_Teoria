# Proyecto 2 Teoría de la Computación

## Integrantes
Maria Marta Ramirez  
Gustavo González

## Instrucciones de uso
Para ejecutar el programa se debe correr el archivo main.py, el cual se encuentra en la carpeta root.
Posteriormente se debe ingresar la gramatica deseada en el archivo de la siguiente
forma:

```python
S = Symbol('S')
A = Symbol('A')
B = Symbol('B')
a = Symbol('a', True)
b = Symbol('b', True)

symbols = {S, A, B, a, b}
terminals = {a, b}
start_symbol = S

S.add_production((A, B), (a,))
A.add_production((b,))
```

En esta instancia estamos ingresando una gramatica $ G = (V, \Sigma, R, S) $  
donde $V = \{S, A, B\}$, $\Sigma = \{a, b\} $, $R = \{ S \rightarrow AB 
| a, A \rightarrow b \}$ y $S = S$


## Neo4j
Para poder utilizar la base de datos Neo4j se debe tener instalado el programa y corriendo en el puerto 7687, 
las credenciales pueden ser modificadas en el archivo de Database.py .