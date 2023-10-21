#from Grammar import Grammar

VARIABLE_INDICATOR = '_'

def view_grammar(grammar):
    for symbol in grammar.symbols:
        if not symbol.is_terminal():
            if symbol.is_terminal():
                print(symbol.symbol, '->', end=' ')
            else:
                print(VARIABLE_INDICATOR + symbol.symbol, '->', end=' ')

            for index, production in enumerate(symbol.productions):
                for production_symbol in production:
                    if production_symbol.is_terminal():
                        print(production_symbol.symbol, end=' ')
                    else:
                        print(VARIABLE_INDICATOR + production_symbol.symbol, end=' ')
                if index != len(symbol.productions) - 1:
                    print('|', end=' ')
            print()
    print()
