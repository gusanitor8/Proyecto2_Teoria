from graphviz import Digraph
import time

class ParseTreeNode:
    def __init__(self, value, children=[]):
        """
        Inicializa un nodo del árbol de análisis sintáctico.

        Args:
            value (str): El valor del nodo, que generalmente representa un símbolo gramatical.
            children (list, opcional): Una lista de nodos hijos. Por defecto, está vacía.
        """
        self.value = value
        self.children = children

    def __repr__(self) -> str:
        """
        Devuelve una representación en cadena del nodo.

        Returns:
            str: El valor del nodo convertido a cadena.
        """
        return self.value

def parse_sentence_cyk(sentence, grammar):
    """
    Realiza un análisis sintáctico de una oración utilizando el algoritmo CYK (Cocke-Younger-Kasami).

    Args:
        sentence (str): La oración de entrada a analizar.
        grammar (dict): Una gramática en forma de diccionario que define las reglas de producción.

    Returns:
        tuple: Una tupla que contiene tres elementos:
            - Un booleano que indica si se pudo analizar la oración.
            - El nodo raíz del árbol de análisis sintáctico.
            - El tiempo de ejecución del análisis en segundos.
    """
    start_time = time.time()
    words = sentence.split()  # Divide la oración en palabras.
    n = len(words)  # Número de palabras en la oración.
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Llena la diagonal de la tabla con símbolos terminales y árboles de análisis.
    for i in range(n):
        word = words[i]
        for symbol, productions in grammar.items():
            for production in productions:
                if len(production) == 1 and production[0] == word:
                    table[i][i].add(ParseTreeNode(symbol, [ParseTreeNode(word)]))

    # Completa la tabla utilizando el algoritmo CYK con árboles de análisis.
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for symbol, productions in grammar.items():
                    for production in productions:
                        if len(production) == 2:
                            A, B = production
                            for left in table[i][k]:
                                for right in table[k + 1][j]:
                                    if B == right.value and A == left.value:
                                        tree = ParseTreeNode(symbol, [left, right])
                                        table[i][j].add(tree)
    end_time = time.time()

    if len(table[0][-1]) != 0:
        # Si hay un árbol de análisis en la celda superior derecha de la tabla,
        # devuelve True junto con el árbol de análisis.
        return True, table[0][-1].pop(), end_time - start_time
    else:
        # Si no se puede analizar la oración, devuelve False y un valor nulo, junto con el tiempo de ejecución.
        return False, None, end_time - start_time

def visualize_parse_tree(root: ParseTreeNode):
    """
    Visualiza el árbol de análisis sintáctico utilizando Graphviz.

    Args:
        root (ParseTreeNode): El nodo raíz del árbol de análisis sintáctico.
    """
    if root is not None:
        graph = Digraph(name='ParseTree', comment='Visualización del Árbol de Análisis Sintáctico')
        build_parse_tree(graph, root)
        graph.view()

def build_parse_tree(dot: Digraph, root: ParseTreeNode, parent_id=None):
    """
    Construye el árbol de análisis sintáctico recursivamente para la visualización.

    Args:
        dot (Digraph): Un objeto Digraph de Graphviz para construir la visualización.
        root (ParseTreeNode): El nodo actual en la construcción del árbol.
        parent_id (str, opcional): El ID del nodo padre. Por defecto, es None.
    """
    node_id = str(id(root))
    dot.node(node_id, str(root.value))
    if parent_id is not None:
        dot.edge(parent_id, node_id)
    for child in root.children:
        build_parse_tree(dot, child, node_id)