import cPickle

class Symbol(object):
    def is_terminal(self):
        return False
    def is_nonterminal(self):
        return False
    def is_empty(self):
        return False

class Terminal(Symbol):
    def __init__(self, token):
        self.token = token
    def is_terminal(self):
        return True
    def __repr__(self):
        return str(self.token)

class Empty(Symbol):
    def __init__(self):
        self.token = 0
    def is_empty(self):
        return True
    def __repr__(self):
        return "Empty"

class Nonterminal(Symbol):
    def __init__(self, id):
        self.id = id
        self.production_rules = []
    def add_production(self, production):
        if len(self.production_rules) > 0:
            index = 0
            for item in self.production_rules:
                if item.get_symbol(0).is_terminal() and not item.get_symbol(0).is_empty():
                    index += 1
                else:
                    break
            if production.is_empty():
                for item in self.production_rules[index:]:
                    if item.get_symbol(0).is_nonterminal() and not item.get_symbol(0).is_empty():
                        index += 1
                    else:
                        break
            self.production_rules.insert(index, production)
        else:
            self.production_rules.append(production)
    def get_expected_symbols(self, rule, index):
        result = []
        if index == 0:
            for i, production in enumerate(self.production_rules):
                result.append((production.get_symbol(index), i, len(self.production_rules)))
        else:
            if rule < len(self.production_rules):
                result.append((self.production_rules[rule].get_symbol(index), rule, 1))
            else:
                result.append((Empty(), rule, 1))
        return result
    def is_nonterminal(self):
        return True
    def __repr__(self):
        return str(self.id) + str (self.production_rules)

class Production(object):
    def __init__(self):
        self.symbols = []
    def add_symbol(self, symbol):
        self.symbols.append(symbol)
    def get_symbol(self, index):
        if not self.is_empty() and index < self.length():
            return self.symbols[index]
        else:
            return Empty()
    def is_empty(self):
        if self.length() == 0:
            return True
        else:
            return False
    def length(self):
        return len(self.symbols)
    def __repr__(self):
        return str(self.symbols)

class Grammar(object):
    def __init__(self):
        self.grammar = {}
    def load(self, table):
        for nonterminal_id in table:
            self.grammar[abs(nonterminal_id)] = Nonterminal(abs(nonterminal_id))
            for production in table[nonterminal_id]:
                new_production = Production()
                for symbol in production:
                    if symbol > 0:
                        new_terminal = Terminal(symbol)
                        new_production.add_symbol(new_terminal)
                    elif symbol < 0:
                        new_nonterminal = Nonterminal(abs(symbol))
                        new_production.add_symbol(new_nonterminal)
                self.grammar[abs(nonterminal_id)].add_production(new_production)
    def serialize(self, file_name):
        with open(file_name, "wb") as file:
            cPickle.dump(self.grammar, file, cPickle.HIGHEST_PROTOCOL)
    def deserialize(self, file_name):
        with open(file_name, "rb") as file:
            return cPickle.load(file)
