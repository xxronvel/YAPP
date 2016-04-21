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

import sys, tokenizer.s_machine, grammar, php_grammar

def parse():
    global nonterminal_id, index, current_rule, is_expected, stack, token
    queue = php.grammar[nonterminal_id].get_expected_symbols(current_rule, index)
    for expected in queue:
        rule_id, symbol, num_rule, total_rules = expected[0], expected[1], expected[2], expected[3]
        print "debug:", nonterminal_id, current_rule, index, symbol
        if symbol.is_terminal():
            if symbol.token == token:
                index += 1
                is_expected = True
                break
            else:
                current_rule += 1
                is_expected = False
        elif symbol.is_nonterminal():
            stack.append((nonterminal_id, index, current_rule, num_rule, total_rules))
            nonterminal_id = symbol.id
            index = 0
            current_rule = 0
            parse()
            break
        else:
            if nonterminal_id != 0:
                last = stack.pop()
                nonterminal_id = last[0]
                index = last[1] + 1
                current_rule = last[2]
                parse()
            break
    else:
        if nonterminal_id != 0:
            last = stack.pop()
            if last[3] < last[4] - 1 and index == 0:
                nonterminal_id = last[0]
                index = 0
                current_rule = last[2] + 1
                parse()

with open(sys.argv[1], "r") as file:
	contents = file.read()
	tokens = tokenizer.s_machine.get_tokens(contents)

php = grammar.Grammar()
php.load(php_grammar.table)
#php.grammar = php.deserialize("grammar.ser").grammar

nonterminal_id = 0
current_rule = 0
index = 0
is_expected = True

stack = []

for item in tokens:
    token, lexeme, line = item[0], item[1], item[2]
    print "%s ========== %s %s ==========" % (line, token, lexeme)
    parse()
    if not is_expected:
        print "Parse error, unexpected \"%s\" on line %s" % (lexeme, line)
        break
else:
    token = 0
    parse()
