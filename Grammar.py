from Variable import EPSILON, Symbol
from View import view_grammar
from typing import Set
from itertools import product
from database import Database

VARIABLE_INDICATOR = '0'


class Grammar:
    def __init__(self, symbols: Set, terminals: Set, start_symbol):
        self.symbols = symbols
        self.terminals = terminals
        self.start_symbol = start_symbol

        self.production_symbol_map = {}
        self.__generate_production_symbol_map()

    def normalize(self):
        # inital grammar
        print("initial grammar")
        view_grammar(self)

        # adding S0 -> S
        print("adding S0 -> S")
        self.__start_var_not_in_rhs()
        view_grammar(self)

        # removing non genarating symbols
        print("removing non generating symbols")
        self.__remove_non_generating_symbols()
        view_grammar(self)

        # removing unreachable symbols
        print("removing unreachable symbols")
        self.__remove_unreachable_symbols()
        view_grammar(self)

        # removing epsilon productions
        print("removing epsilon productions")
        nullable_vars = self.get_nullable_vars()
        new_symbols = self.__remove_epsilon_productions(nullable_vars)
        self.symbols = new_symbols
        view_grammar(self)

        # eliminating unit rules
        print("eliminating unit rules")
        db = Database()
        self.eliminate_unit_rules(db)
        view_grammar(self)
        db.clear_database()

        # single terminal production form
        print("single terminal production form")
        self.__create_terminal_vars()
        self.__replace_terminals()
        view_grammar(self)

    def __remove_non_generating_symbols(self):
        generating_symbols = self.__produces()

        new_symbols = set()
        for symbol in self.symbols:  # iterar sobree cada simbolo
            new_productions = set()
            if symbol in generating_symbols:
                for production in symbol.productions:  # iterar sobre cada produccion del simbolo
                    if any(symbols not in generating_symbols for symbols in production):
                        continue
                    else:
                        new_productions.add(production)

                symbol.productions = new_productions
                new_symbols.add(symbol)

        self.symbols = new_symbols

    def __remove_unreachable_symbols(self):
        reachable_symbols = self.__reachable()

        new_symbols = set()
        for symbol in self.symbols:
            if symbol in reachable_symbols:
                new_symbols.add(symbol)

        self.symbols = new_symbols

    def __create_terminal_vars(self):
        terminals = self.__terminal_vars_needed()
        for terminal in terminals:
            if terminal.symbol != EPSILON:
                new_symbol = Symbol(terminal.symbol)
                new_symbol.add_production((terminal,))
                self.symbols.add(new_symbol)

    def __terminal_vars_needed(self):
        terminal_vars_needed = set()
        for symbol in self.symbols:
            for production in symbol.productions:
                for production_symbol in production:
                    if production_symbol.is_terminal() and len(production) > 1:
                        terminal_vars_needed.add(production_symbol)

        return terminal_vars_needed

    def __replace_terminals(self):
        for symbol in self.symbols:
            new_productions = set()
            for production in symbol.productions:
                if len(production) > 1:
                    new_production = []
                    for production_symbol in production:
                        if production_symbol.is_terminal():
                            new_symbol = Symbol.variable_map[production_symbol.symbol]
                            new_production.append(new_symbol)
                        else:
                            new_production.append(production_symbol)
                    new_productions.add(tuple(new_production))
                else:
                    new_productions.add(production)
            symbol.productions = new_productions

    def eliminate_unit_rules(self, db: Database):
        db.instanciate_nodes(self.symbols)

        for symbol in self.symbols:
            reachable_unit_rules_ids = db.get_reachable_nodes(symbol)

            if reachable_unit_rules_ids:
                reachable_unit_rules = [Symbol.node_map[symbol_id] for symbol_id in reachable_unit_rules_ids]
                reachable_unit_rules: Set[Symbol] = set(reachable_unit_rules)

                for unit_rule in reachable_unit_rules:
                    if symbol != unit_rule:
                        symbol.productions = symbol.productions.union(unit_rule.productions)

        self.__remove_unit_rules()

    def __remove_unit_rules(self):
        for symbol in self.symbols:
            new_productions = set()
            for production in symbol.productions:
                if not (len(production) == 1 and not production[0].is_terminal()):
                    new_productions.add(production)
            symbol.productions = new_productions

    def __start_var_not_in_rhs(self):
        """
        Este metodo agrega una nueva produccion S0 -> S
        de forma que nustra variable inicial no esta del lado derecho
        :return:
        """
        s0 = Symbol('S0')
        s0.add_production((self.start_symbol,))
        self.symbols.add(s0)

    def __generate_production_symbol_map(self):
        """
        Esta función genera un hashmap donde la llave es la produccion y el valor es el simbolo que la produce
        :return: None
        """
        for symbol in self.symbols:
            for production in symbol.productions:
                self.production_symbol_map[production] = symbol

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
        Este metodo devuelve los nuevas producciones de la gramatica sin epsilon
        :return: set de simbolos con las producciones epsilon eliminadas
        """

        new_symbols = set()

        for symbol in self.symbols:
            new_symbol = Symbol(symbol=symbol.get_symbol(), is_terminal=symbol.is_terminal())
            for production in symbol.productions:
                nullable = [symbol for symbol in production if symbol in nulable_vars]
                if nullable:
                    permuted_nullables = self.__permutate(nullable)
                    new_productions = self.__generate_new_productions(permuted_nullables, production, nullable)
                    new_productions = new_productions.union(symbol.productions)
                    new_productions = self.__remove_epsilon(new_productions)
                    new_symbol.add_productions(new_productions)
                else:
                    if symbol.get_symbol() != EPSILON and len(production) > 0:
                        if production[0].get_symbol() != EPSILON:
                            new_symbol.add_production(production)

            if new_symbol.get_symbol() != EPSILON:
                new_symbols.add(new_symbol)

        return new_symbols

    @staticmethod
    def __remove_epsilon(productions: set):
        new_productions = set()
        for production in productions:
            for symbol in production:  # TODO revisar si puede existir epsilon junto con otros simbolos
                if not symbol.get_symbol() == EPSILON:
                    new_productions.add(production)
                    break

        return new_productions

    def __generate_new_productions(self, permuted_nullable, original_production: tuple, nullable_vars):
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
                # TODO arreglar bug, se debe revisar si es anulable, no si es terminal
                if symbol not in nullable_vars:
                    production.append(symbol)
                else:
                    new_symbol = tupla.pop(0)
                    if new_symbol is not None:
                        production.append(new_symbol)
            if len(production) > 0:
                new_productions.add(tuple(production))

        return new_productions

    def __permutate(self, nullable_tuple: list):
        """
        Genera un array de tuplas con todas las combinaciones posibles de las variables anulables
        :param nullable_tuple: una lista de todas las variables anulables
        :return: list
        """
        nullable_tuple = list(nullable_tuple)
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

    def to_dict(self) -> dict[str, list[list[str]]]:
        """
        Convierte la gramatica a un diccionario
        :return: dict
        """
        dictionarized_grammar = {}

        for symbol in self.symbols:
            if not symbol.is_terminal() and symbol.productions:
                if symbol.is_terminal():
                    dictionarized_grammar[symbol.symbol] = []
                else:
                    dictionarized_grammar[VARIABLE_INDICATOR + symbol.symbol] = []

                for index, production in enumerate(symbol.productions):
                    new_production = []

                    for production_symbol in production:
                        if production_symbol.is_terminal():
                            new_production.append(production_symbol.symbol)
                        else:
                            new_production.append(VARIABLE_INDICATOR + production_symbol.symbol)

                    if symbol.is_terminal():
                        dictionarized_grammar[symbol.symbol].append(new_production)
                    else:
                        dictionarized_grammar[VARIABLE_INDICATOR + symbol.symbol].append(new_production)

        return dictionarized_grammar
