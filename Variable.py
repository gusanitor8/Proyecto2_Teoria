import typing

EPSILON = 'ε'


class Symbol:
    def __init__(self, symbol=EPSILON, is_terminal=False):
        self.symbol = symbol
        self.isTerminal = is_terminal
        self.productions = set()

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


class Variable(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)
