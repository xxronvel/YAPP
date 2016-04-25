# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2016 Aarón Abraham Velasco Alvarez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pickle as pickle

class Symbol(object):
    def is_terminal(self):
        return False
    def is_nonterminal(self):
        return False
    def is_empty(self):
        return False

class Terminal(Symbol):
    def __init__(self, token, pattern_id):
        self.token = token
        self.pattern_id = pattern_id
        self.trace = []
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
        self.sequence = 0

    def add_production(self, production):
        if len(self.production_rules) > 0:
            index = 0
            for item in self.production_rules:
                if item.get_symbol(0).is_terminal():
                    index += 1
                else:
                    break
            if production.is_empty():
                for item in self.production_rules[index:]:
                    if item.get_symbol(0).is_nonterminal():
                        index += 1
                    else:
                        break
            self.production_rules.insert(index, production)
        else:
            self.production_rules.append(production)
        self.sequence += 1

    def get_expected_symbols(self, rule, index):
        result = []
        if index == 0:
            for n, production in enumerate(self.production_rules[rule:], rule):
                result.append((production.id, production.get_symbol(index), n, len(self.production_rules)))
        else:
            if rule < len(self.production_rules):
                result.append((self.production_rules[rule].id, self.production_rules[rule].get_symbol(index), rule, 1))
            else:
                result.append((0, Empty(), rule, 1))
        return result

    def get_expected_symbols_(self, rule, index, checked):
        result = []
        rule = self.get_production_index(rule)
        if index == 0:
            for n, production in enumerate(self.production_rules):
                if not production.id in checked:
                    result.append((production.id, production.get_symbol(index), n, len(self.production_rules)))
        else:
            if rule < len(self.production_rules):
                result.append((self.production_rules[rule].id, self.production_rules[rule].get_symbol(index), rule, 1))
            else:
                result.append((0, Empty(), rule, 1))
        return result

    def get_production_index(self, id):
        result = None
        for n, rule in enumerate(self.production_rules):
            if rule.id == id:
                result = n
                break
        return result

    def insert_token(self, rule, index, token, indices, inserting, pattern_id):
        rule = self.get_production_index(rule)
        if index == 0:
            new_production = Production(self.sequence)
            if not token == 0:
                new_production.add_symbol(Terminal(token, pattern_id))
            self.add_production(new_production)
            return (0, self)
        elif index < self.production_rules[rule].length():
            new_production1 = Production(self.production_rules[rule].id)
            new_production2 = Production(0)
            new_production3 = Production(1)
            for symbol in self.production_rules[rule].get_items()[:index]:
                new_production1.add_symbol(symbol)
            new_production1.add_symbol(Nonterminal(indices))
            for symbol in self.production_rules[rule].get_items()[index:]:
                new_production2.add_symbol(symbol)
            if not token == 0:
                new_production3.add_symbol(Terminal(token, pattern_id))
            self.del_production(rule)
            self.add_production(new_production1)
            new_nonterminal = Nonterminal(indices)
            new_nonterminal.add_production(new_production2)
            new_nonterminal.add_production(new_production3)
            return (1, new_nonterminal)
        elif index == self.production_rules[rule].length() and inserting:
            if not token == 0:
                self.production_rules[rule].add_symbol(Terminal(token, pattern_id))
            return (2, self)
        else:
            if not self.production_rules[rule].is_empty():
                self.production_rules[rule].add_symbol(Nonterminal(indices))
            else:
                new_production = Production(self.sequence)
                new_production.add_symbol(Nonterminal(indices))
                self.add_production(new_production)
            new_production = Production(0)
            if not token == 0:
                new_production.add_symbol(Terminal(token, pattern_id))
            new_nonterminal = Nonterminal(indices)
            new_nonterminal.add_production(new_production)
            new_nonterminal.add_production(Production(1))
            return (3, new_nonterminal)

    def del_production(self, rule):
        del self.production_rules[rule]

    def set_trace(self, rule, index, trace):
        rule = self.get_production_index(rule)
        self.production_rules[rule].symbols[index].trace = trace

    def get_trace(self, rule, index):
        return self.production_rules[rule].symbols[index].trace

    def is_nonterminal(self):
        return True

    def __repr__(self):
        return str(self.id) + str (self.production_rules)

class Production(object):
    def __init__(self, id):
        self.id = id
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

    def get_items(self):
        return self.symbols

    def length(self):
        return len(self.symbols)

    def __repr__(self):
        return str(self.symbols)

class Grammar(object):
    def __init__(self):
        self.grammar = {}
        self.patterns = 0
    def load(self, table):
        for nonterminal_id in table:
            self.grammar[nonterminal_id] = Nonterminal(nonterminal_id)
            for n, production in enumerate(table[nonterminal_id]):
                new_production = Production(n)
                for symbol in production:
                    if symbol > 0:
                        new_production.add_symbol(Terminal(symbol, 0))
                    elif symbol < 0:
                        new_production.add_symbol(Nonterminal(abs(symbol)))
                self.grammar[nonterminal_id].add_production(new_production)

    def add_nonterminal(self, nonterminal):
        self.grammar[nonterminal.id] = nonterminal

    def get_patterns(self):
        self.patterns += 1
        return self.patterns

    def get_indices(self):
        return len(self.grammar)

    def serialize(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    def deserialize(self, file_name):
        with open(file_name, "rb") as file:
            return pickle.load(file)
