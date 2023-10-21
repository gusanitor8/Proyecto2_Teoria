import typing

EPSILON = 'ε'


class Symbol:
    next_id = 0
    node_map = {}

    def __init__(self, symbol=EPSILON, is_terminal=False):
        self.symbol = symbol
        self.isTerminal = is_terminal
        self.productions = set()
        self.id = Symbol.next_id

        # globals
        Symbol.node_map[self.id] = self
        Symbol.next_id += 1

    @staticmethod
    def get_node(node_id: int):
        try:
            return Symbol.node_map[node_id]
        except KeyError:
            # TODO revisar el return para evitar errores
            return None

    def __contains__(self, item):
        for production in self.productions:
            return any(item in production for item in production)

    def add_production(self, *productions):
        for production in productions:
            self.productions.add(production)

    def add_productions(self, productions: set):
        self.productions = productions

    def get_symbol(self):
        """
        Devuelve el simbolo de la variable
        :return: str
        """
        return self.symbol

    def is_nullable(self) -> bool:
        """
        Indica si la variable es anulable en UN SOLO paso
        :return: Boolean
        """

        for production in self.productions:
            nullable = any(EPSILON == symbol.get_symbol() for symbol in production)
            if nullable:
                return True

        return False

    def is_terminal(self):
        return self.isTerminal

    def get_unit_productions(self):
        """
        Devuelve las producciones unitarias de la variable
        :return: set
        """
        unit_productions = set()
        for production in self.productions:
            if len(production) == 1 and not production[0].is_terminal():
                unit_productions.add(production)

        return unit_productions

    def __str__(self):
        return f'nodo-{self.id}:Symbol{{symbol: {self.symbol} }}'


class Variable(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)
