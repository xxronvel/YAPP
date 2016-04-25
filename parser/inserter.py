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

"""
TODO Insertar funciones
"""
import php_grammar

class Inserter(object):
    def __init__(self, grammar, verbose):
        self.grammar = grammar
        self.verbose = verbose
        self.pattern_id = self.grammar.get_patterns()
        self.nonterminal_id = 0
        self.current_rule = 0
        self.index = 0
        self.inserting = False
        self.stack = []
        self.checked = []
        self.instructions = 0
        self.terminated = False
        self.pattern = 0
        self.trace = []

    def go_back(self, token):
        if self.nonterminal_id != 0:
            last = self.stack.pop()
            self.nonterminal_id = last[0]
            self.index = last[1] + 1
            self.checked = last[2]
            self.current_rule = last[5]
            self.insert(token)

    def insert_token(self, token, num_rule, total_rules):
        inserted, nonterminal = self.grammar.grammar[self.nonterminal_id].insert_token(self.current_rule,
                                                                                       self.index,
                                                                                       token,
                                                                                       self.grammar.get_indices(),
                                                                                       self.inserting,
                                                                                       self.pattern_id)
        self.grammar.add_nonterminal(nonterminal)
        if not self.nonterminal_id == nonterminal.id:
            self.stack.append((self.nonterminal_id,
                               self.index,
                               self.checked,
                               num_rule,
                               total_rules,
                               self.current_rule))
            self.nonterminal_id = nonterminal.id
        if inserted == 1 or inserted == 3:
            self.checked = []
            self.index = 0
        self.insert(token)

    def insert(self, token):
        queue = self.grammar.grammar[self.nonterminal_id].get_expected_symbols_(self.current_rule,
                                                                                self.index,
                                                                                self.checked)
        symbol, num_rule, total_rules = None, None, None
        for expected in queue:
            self.current_rule, symbol, num_rule, total_rules = expected[0], expected[1], expected[2], expected[3]
            if self.verbose >= 3:
                print "debug:", self.nonterminal_id, self.current_rule, self.index, symbol, self.inserting
            if symbol.is_terminal():
                if symbol.token == token:
                    if token == php_grammar.separator or token in php_grammar.closing_tags:
                        self.terminated = True
                    if not self.terminated:
                        self.pattern = symbol.pattern_id
                        self.grammar.grammar[self.nonterminal_id].set_trace(self.current_rule,
                                                                            self.index,
                                                                            self.trace)
                        if (not token in php_grammar.opening_tags):
                            self.trace.append(token)
                    self.index += 1
                    break
                else:
                    self.checked.append(self.current_rule)
                    self.inserting = False
            elif symbol.is_nonterminal():
                self.stack.append((self.nonterminal_id,
                                   self.index,
                                   self.checked,
                                   num_rule,
                                   total_rules,
                                   self.current_rule))
                self.nonterminal_id = symbol.id
                self.index = 0
                self.checked = []
                self.inserting = False
                self.insert(token)
                break
            else:
                if not self.inserting:
                    self.go_back(token)
                else:
                    if not (token == php_grammar.separator or token in php_grammar.closing_tags):
                        self.insert_token(token, num_rule, total_rules)
                        self.inserting = True
                    else:
                        self.terminated = True
                        self.inserting = False
                        self.go_back(token)
                break
        else:
            if self.nonterminal_id != 0:
                last = self.stack.pop()
                if last[3] < last[4] - 1 and self.index == 0:
                    self.nonterminal_id = last[0]
                    self.index = 0
                    self.checked = last[2]
                    self.checked.append(last[5])
                    self.insert(token)
                else:
                    if not (token == php_grammar.separator or token in php_grammar.closing_tags):
                        self.stack.append(last)
                        self.insert_token(token, num_rule, total_rules)
                        self.inserting = True
                    else:
                        self.terminated = True
                        self.inserting = False
                        self.nonterminal_id = last[0]
                        self.index = last[1] + 1
                        self.checked = last[2]
                        self.current_rule = last[5]
                        self.insert_token(0, num_rule, total_rules)
            else:
                self.insert_token(token, num_rule, total_rules)
                self.inserting = True

    def run(self, tokens):
        is_php = False
        for item in tokens:
            token, lexeme = item[0], item[1]
            if token in php_grammar.opening_tags:
                is_php = True
            elif token in php_grammar.closing_tags:
                is_php = False

            if is_php or token in php_grammar.closing_tags:
                if self.verbose >= 3:
                    print "========== %s %s ==========" % (token, lexeme)
                self.insert(token)
                if self.terminated:
                    if self.pattern == self.pattern_id:
                        self.instructions += 1
                    self.terminated = False
                    if self.verbose >= 3:
                        print "Pattern:", self.pattern, len(self.trace), self.trace
                    self.pattern = 0
                    self.trace = []
