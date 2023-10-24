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

En esta instancia, estamos definiendo una gramática \(G = (V, \Sigma, R, S)\) donde:

- \(V = \{S, A, B\}\)
- \(\Sigma = \{a, b\}\)
- \(R = \{ S \rightarrow AB | a, A \rightarrow b \}\)
- \(S\) es el símbolo inicial.


## Neo4j
Para poder utilizar la base de datos Neo4j se debe tener instalado el programa y corriendo en el puerto 7687, 
las credenciales pueden ser modificadas en el archivo de Database.py .

# Discusión

## Diseño de la Aplicación
En el proceso de desarrollo de nuestra aplicación, se ha seguido un diseño orientado a objetos que permite la manipulación y normalización de gramáticas libres de contexto (CFG) en la Chomsky Normal Form (CNF). El diseño se centra en dos clases principales: Grammar y Symbol, cada una de las cuales cumple un papel fundamental en el proceso de transformación.

Clase `Grammar`:  
La clase Grammar almacena y gestiona toda la información relacionada con una gramática. Contiene las siguientes propiedades y métodos clave:

* terminals y nonTerminals: Propiedades que almacenan los símbolos terminales y no terminales de la gramática, respectivamente.

* startSymbol: Propiedad que guarda el símbolo inicial de la gramática.

* productions: Un conjunto de producciones, donde cada producción se asocia a un símbolo no terminal.

* Métodos para realizar las siguientes tareas:

  * Añadir producciones.
  * Encontrar símbolos inalcanzables y eliminarlos.
  * Eliminar producciones unitarias.
  * Eliminar producciones vacías.
  * Normalizar las producciones a la CNF.
  
Clase `Symbol`
La clase Symbol es utilizada para representar tanto símbolos terminales como no terminales. Cada instancia de esta clase contiene un conjunto de producciones que se asocian al símbolo que representa.

__Uso de Neo4j para Producciones Unitarias__  
Para resolver el problema de encontrar y eliminar producciones unitarias, nuestra aplicación hace uso de una base de datos Neo4j. Se utiliza la clase Database para instanciar todos los nodos que representan producciones unitarias. Luego, mediante consultas (queries), se obtienen todas las producciones unitarias alcanzables en la gramática.

## Discusión
Durante el proceso de desarrollo, se encontraron varios desafíos. Uno de los desafíos más destacados fue la detección y eliminación de producciones unitarias. El uso de una base de datos Neo4j se consideró necesario para manejar eficazmente las producciones unitarias alcanzables, ya que este proceso puede ser complejo en gramáticas más grandes.

## Recomendaciones
Para mejorar la eficiencia y escalabilidad de la aplicación, se podría considerar la implementación de algoritmos más eficientes para la eliminación de producciones unitarias. Además, se pueden agregar más funciones y validaciones para garantizar que las gramáticas de entrada se ajusten a los requisitos de una CFG y simplificar aún más el proceso de normalización.

## Ejemplos y Pruebas Realizadas
A lo largo del desarrollo, se realizaron pruebas exhaustivas utilizando diversas gramáticas de prueba. Estas pruebas se centraron en verificar la capacidad de la aplicación para convertir gramáticas en CNF y asegurar que el resultado sea correcto. Se utilizaron gramáticas de diferentes tamaños y complejidades para evaluar el rendimiento y la precisión de la aplicación.

Espero que esta estructura te sea útil para redactar la sección de diseño de tu aplicación. Si tienes más detalles o deseas agregar información adicional, no dudes en proporcionarla para personalizar aún más esta sección.