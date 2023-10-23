# from Grammar import Grammar

VARIABLE_INDICATOR = '0'


def view_grammar(grammar):
    for symbol in grammar.symbols:
        if not symbol.is_terminal() and symbol.productions:
            if symbol.is_terminal():
                print(symbol.symbol, '->', end=' ')
            else:
                print(symbol.symbol + VARIABLE_INDICATOR, '->', end=' ')

            for index, production in enumerate(symbol.productions):
                for production_symbol in production:
                    if production_symbol.is_terminal():
                        print(production_symbol.symbol, end=' ')
                    else:
                        print(production_symbol.symbol + VARIABLE_INDICATOR, end=' ')
                if index != len(symbol.productions) - 1:
                    print('|', end=' ')
            print()
    print()
