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

import php_grammar
from sets import Set

class Parser(object):
    def __init__(self, grammar, verbose):
        self.grammar = grammar
        self.verbose = verbose
        self.nonterminal_id = 0
        self.current_rule = 0
        self.index = 0
        self.is_expected = True
        self.stack = []
        self.pattern = 0
        self.patterns = Set()
        self.pattern_trace = {}
        self.instructions = {}
        self.trace = []
        self.terminated = False
        self.script = '<?php\n'
        self.snippets = []

    def parse(self, token, lexeme, line):
        queue = self.grammar.grammar[self.nonterminal_id].get_expected_symbols(self.current_rule,
                                                                      self.index)
        for expected in queue:
            rule_id, symbol, num_rule, total_rules = expected[0], expected[1], expected[2], expected[3]
            if self.verbose >= 3:
                print "debug:", self.nonterminal_id, self.current_rule, self.index, symbol
            if symbol.is_terminal():
                if symbol.token == token:
                    if token == php_grammar.separator or token in php_grammar.closing_tags:
                        self.terminated = True
                    if not self.terminated:
                        self.pattern = symbol.pattern_id
                        self.pattern_trace[self.pattern] = self.grammar.grammar[self.nonterminal_id].get_trace(self.current_rule,
                                                                                                               self.index)
                        if (not token in php_grammar.opening_tags):
                            self.trace.append((token, lexeme, line))
                    self.index += 1
                    self.is_expected = True
                    break
                else:
                    self.current_rule += 1
                    self.is_expected = False
            elif symbol.is_nonterminal():
                self.stack.append((self.nonterminal_id,
                                   self.index,
                                   self.current_rule,
                                   num_rule,
                                   total_rules))
                self.nonterminal_id = symbol.id
                self.index = 0
                self.current_rule = 0
                self.parse(token, lexeme, line)
                break
            else:
                if self.nonterminal_id != 0:
                    last = self.stack.pop()
                    self.nonterminal_id = last[0]
                    self.index = last[1] + 1
                    self.current_rule = last[2]
                    self.parse(token, lexeme, line)
                break
        else:
            if self.nonterminal_id != 0:
                last = self.stack.pop()
                if last[3] < last[4] - 1 and self.index == 0:
                    self.nonterminal_id = last[0]
                    self.index = 0
                    self.current_rule = last[2] + 1
                    self.parse(token, lexeme, line)

    def run(self, tokens):
        result = True
        is_php = False
        for item in tokens:
            token, lexeme, line = item[0], item[1], item[2]
            if token in php_grammar.opening_tags:
                is_php = True
            elif token in php_grammar.closing_tags:
                is_php = False

            if (is_php or token in php_grammar.closing_tags) and not token in php_grammar.ignored_tokens:
                if self.verbose >= 3:
                    print "{} ========== {} {} ==========".format(line, token, lexeme)
                self.parse(token, lexeme, line)
                if self.terminated:
                    if not self.pattern == 0:
                        if [ t[0] for t in self.trace] == self.pattern_trace[self.pattern]:
                            self.patterns.add(self.pattern)
                        if self.instructions.get(self.pattern, None) != None:
                            self.instructions[self.pattern] += 1
                        else:
                            self.instructions[self.pattern] = 1
                        self.eval_prefix(self.trace)
                    else:
                        self.built_script(self.trace)
                    if not token in php_grammar.closing_tags:
                        if token != php_grammar.separator:
                            self.script += '{} '.format(lexeme)
                        else:
                            self.script += '{}\n'.format(lexeme)
                    else:
                        self.script += '\n?>'
                    self.terminated = False
                    self.pattern = 0
                    self.trace = []
                if not self.is_expected:
                    #TODO
                    print "Parse error, unexpected \"{}\" on line {}".format(lexeme, line)
                    result = False
                    break
        else:
            token = 0
            lexemes = ''
            line = 0
            self.parse(token, lexeme, line)
        return result

    def built_script(self, lexemes):
        for lexeme in lexemes:
            self.script += '{} '.format(lexeme[1])

    def eval(self, lexemes):
        string_function = False
        obfuscated = ''
        in_brackets = []
        line = None
        for item in lexemes:
            token, lexeme = item[0], item[1]
            self.script += '{} '.format(lexeme)
            if string_function:
                obfuscated += '{} '.format(lexeme)
                if token == php_grammar.round_brackets[0]:
                    in_brackets.append(token)
                elif token == php_grammar.round_brackets[1]:
                    top = in_brackets.pop()
                    if len(in_brackets) == 0:
                        self.snippets.append((obfuscated, line))
                        string_function = False
            elif token in php_grammar.string_functions:
                obfuscated += lexeme
                string_function = True
                line = item[2]

    def eval_prefix(self, lexemes):
        operands = []
        operators = []
        for item in lexemes[::-1]:
            token, lexeme = item[0], item[1]
            if not token in php_grammar.assignment_operators:
                operands.append(item)
            else:
                while len(operators) > 0:
                    top = operators.pop()
                    operands.append(top)
                else:
                    operators.append(item)
        else:
            while len(operators) > 0:
                top = operators.pop()
                operands.append(top)

        if not operands[-1][0] in php_grammar.assignment_operators:
            self.script += '#'
        string_function = False
        obfuscated = ''
        in_brackets = []
        line = None
        for item in lexemes:
            token, lexeme = item[0], item[1]
            self.script += '{} '.format(lexeme)
            if string_function:
                obfuscated += '{} '.format(lexeme)
                if token == php_grammar.round_brackets[0]:
                    in_brackets.append(token)
                elif token == php_grammar.round_brackets[1]:
                    top = in_brackets.pop()
                    if len(in_brackets) == 0:
                        self.snippets.append((obfuscated, line))
                        string_function = False
            elif token in php_grammar.string_functions:
                obfuscated += lexeme
                string_function = True
                line = item[2]
