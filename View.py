# from Grammar import Grammar


def view_grammar(grammar):
    for symbol in grammar.symbols:
        if not symbol.is_terminal():
            print(symbol.symbol, '->', end=' ')

            for index, production in enumerate(symbol.productions):
                for production_symbol in production:
                    print(production_symbol.symbol, end=' ')
                if index != len(symbol.productions) - 1:
                    print('|', end=' ')
            print()
    print()
