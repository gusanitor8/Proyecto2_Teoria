from Variable import EPSILON, Symbol
from typing import Set
from itertools import product


class Grammar:
    def __init__(self, symbols: Set, terminals: Set, start_symbol):
        self.symbols = symbols
        self.terminals = terminals
        self.start_symbol = start_symbol

        self.production_symbol_map = {}
        self.__generate_production_symbol_map()

        producing_vars = self.__produces()
        reachable_vars = self.__reachable()
        nulable_vars = self.get_nullable_vars()
        self.__remove_epsilon_productions(nulable_vars)

    def __generate_production_symbol_map(self):
        """
        Esta función genera un hashmap donde la llave es la produccion y el valor es el simbolo que la produce
        :return: None
        """
        for symbol in self.symbols:
            for production in symbol.productions:
                self.production_symbol_map[production] = symbol

    def normalize(self):
        pass

    def eliminate_useless_symbols(self):
        pass

    def __produces(self):
        """
        Este metodo genera el conjunto de simbolos que producen de la gramatica
        :return: el conjunto de elementos que producen de la gramatica
        """
        w = self.terminals
        w_prime = set()

        while w != w_prime:
            w_prime = w
            for symbol in self.symbols:
                for production in symbol.productions:
                    if all(symbols in w_prime for symbols in production):
                        w = w.union({symbol})

        return w

    def __reachable(self):
        """
        Este metodo genera el conjunto de simbolos que son alcanzables desde el simbolo inicial
        :return: conjunto de simbolos alcanzables desde el simbolo inicial
        """
        w = {self.start_symbol}
        w_prime = set()

        while w != w_prime:
            w_prime = w
            for symbols in w_prime:
                for production in symbols.productions:
                    reachable_symbols = set(production)
                    w = w.union(reachable_symbols)

        return w

    def get_nullable_vars(self):
        """
        Este metodo genera el conjunto de simbolos que son anulables en 0 o mas pasos
        :return: set de simbolos anulables
        """
        flag = True
        w = set()

        for production in self.symbols:
            if production.is_nullable():
                w = w.union({production})

        while flag:
            flag = False
            for symbol in self.symbols:
                if symbol in w:
                    continue

                for production in symbol.productions:
                    if all(symbols in w for symbols in production):
                        w = w.union({symbol})
                        flag = True
                        break
                if flag:
                    break
        return w

    def __remove_epsilon_productions(self, nulable_vars: Set):
        """
        Este metodo elimina las producciones epsilon de la gramatica
        :return: set de simbolos con las producciones epsilon eliminadas
        """

        new_symbols = set()

        for symbol in self.symbols:
            new_symbol = Symbol(symbol=symbol.get_symbol(), is_terminal=symbol.is_terminal())
            for production in symbol.productions:
                nullable = [symbol for symbol in production if symbol in nulable_vars]
                if nullable:
                    permuted_nullables = self.__permutate(nullable)
                    new_productions = self.__generate_new_productions(permuted_nullables, production)
                    new_productions = new_productions.union(symbol.productions)
                    new_productions = self.__remove_epsilon(new_productions)
                    new_symbol.add_productions(new_productions)
                else:
                    if symbol.get_symbol() != EPSILON:
                        new_symbol.add_production(production)

            if new_symbol.get_symbol() != EPSILON:
                new_symbols.add(new_symbol)

        return new_symbols

    @staticmethod
    def __remove_epsilon(productions: set):
        for production in productions:
            for symbol in production:  # TODO revisar si puede existir epsilon junto con otros simbolos
                if symbol.get_symbol() == EPSILON:
                    productions.remove(production)
                    return productions

        return productions

    def __generate_new_productions(self, permuted_nullable, original_production: tuple):
        """
        Genera las nuevas producciones con base en una produccion y las variables anulables
        :param permuted_nullable: conjunto de tuplas con las variables anulables permutadas
        :param original_production: tupla de la produccion original
        :return: conjunto con todas las nuevas producciones
        """
        new_productions = set()
        for tupla in permuted_nullable:
            production = []
            for symbol in original_production:
                if symbol.is_terminal():
                    production.append(symbol)
                else:
                    new_symbol = tupla.pop(0)
                    if new_symbol is not None:
                        production.append(new_symbol)

            new_productions.add(tuple(production))

        return new_productions

    def __permutate(self, nullable_tuple: list):
        """
        Genera un array de tuplas con todas las combinaciones posibles de las variables anulables
        :param nullable_tuple: una lista de todas las variables anulables
        :return: list
        """
        length = len(nullable_tuple)
        boolean_combinations = self.__generate_boolean_combinations(length)
        new_tuples = []
        for combination in boolean_combinations:
            tupla = []
            for index, value in enumerate(combination):
                if value:
                    tupla.append(nullable_tuple[index])
                else:
                    tupla.append(None)
            new_tuples.append(tupla)

        return new_tuples

    @staticmethod
    def __generate_boolean_combinations(n: int):
        """
        Genera todas las combinaciones posibles de arrays booleanos de tamaño n
        :param n: tamaño del array
        :return: list de arrays booleanos
        """
        if n <= 0:
            return [[]]

        boolean_values = [True, False]
        boolean_combinations = list(product(boolean_values, repeat=n))

        return boolean_combinations
