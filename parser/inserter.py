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
import sys, tokenizer.s_machine, grammar, php_grammar

def insert_pattern():
    global nonterminal_id, index, current_rule, stack, token, terminated, pattern, inserting, pattern_id, checked, trace
    queue = php.grammar[nonterminal_id].get_expected_symbols_(current_rule, index, checked)
    symbol, num_rule, total_rules = None, None, None
    for expected in queue:
        current_rule, symbol, num_rule, total_rules = expected[0], expected[1], expected[2], expected[3]
        print "debug:", nonterminal_id, current_rule, index, symbol, inserting
        if symbol.is_terminal():
            if symbol.token == token:
                if token == separator or token in closing_tags:
                    terminated = True
                if not terminated:
                    pattern = symbol.pattern_id
                    php.grammar[nonterminal_id].set_trace(current_rule, index, trace)
                    if (not token in opening_tags):
                        trace.append((nonterminal_id, current_rule, index))
                index += 1
                break
            else:
                checked.append(current_rule)
                inserting = False
        elif symbol.is_nonterminal():
            stack.append((nonterminal_id, index, checked, num_rule, total_rules, current_rule))
            nonterminal_id = symbol.id
            index = 0
            checked = []
            inserting = False
            insert_pattern()
            break
        else:
            if not inserting:
                if nonterminal_id != 0:
                    last = stack.pop()
                    nonterminal_id = last[0]
                    index = last[1] + 1
                    checked = last[2]
                    current_rule = last[5]
                    insert_pattern()
            else:
                if not (token == separator or token in closing_tags):
                    inserted, nonterminal = php.grammar[nonterminal_id].insert_token(current_rule, index, token, php.get_indices(), inserting, pattern_id)
                    php.add_nonterminal(nonterminal)
                    if not nonterminal_id == nonterminal.id:
                        stack.append((nonterminal_id, index, checked, num_rule, total_rules, current_rule))
                        nonterminal_id = nonterminal.id
                    if inserted == 1 or inserted == 3:
                        checked = []
                        index = 0
                    insert_pattern()
                    inserting = True
                else:
                    terminated = True
                    inserting = False
                    if nonterminal_id != 0:
                        last = stack.pop()
                        nonterminal_id = last[0]
                        index = last[1] + 1
                        checked = last[2]
                        current_rule = last[5]
                        insert_pattern()
            break
    else:
        if nonterminal_id != 0:
            last = stack.pop()
            if last[3] < last[4] - 1 and index == 0:
                nonterminal_id = last[0]
                index = 0
                checked = last[2]
                checked.append(last[5])
                insert_pattern()
            else:
                if not (token == separator or token in closing_tags):
                    stack.append(last)
                    inserted, nonterminal = php.grammar[nonterminal_id].insert_token(current_rule, index, token, php.get_indices(), inserting, pattern_id)
                    php.add_nonterminal(nonterminal)
                    if not nonterminal_id == nonterminal.id:
                        stack.append((nonterminal_id, index, checked, num_rule, total_rules, current_rule))
                        nonterminal_id = nonterminal.id
                    if inserted == 1 or inserted == 3:
                        checked = []
                        index = 0
                    insert_pattern()
                    inserting = True
                else:
                    terminated = True
                    inserting = False
                    nonterminal_id = last[0]
                    index = last[1] + 1
                    checked = last[2]
                    current_rule = last[5]
                    inserted, nonterminal = php.grammar[nonterminal_id].insert_token(current_rule, index, 0, php.get_indices(), inserting, pattern_id)
                    php.add_nonterminal(nonterminal)
                    if not nonterminal_id == nonterminal.id:
                        stack.append((nonterminal_id, index, checked, num_rule, total_rules, current_rule))
                        nonterminal_id = nonterminal.id
                    if inserted == 1 or inserted == 3:
                        checked = []
                        index = 0
                    insert_pattern()
        else:
            inserted, nonterminal = php.grammar[nonterminal_id].insert_token(current_rule, index, token, php.get_indices(), inserting, pattern_id)
            php.add_nonterminal(nonterminal)
            if not nonterminal_id == nonterminal.id:
                stack.append((nonterminal_id, index, checked, num_rule, total_rules, current_rule))
                nonterminal_id = nonterminal.id
            if inserted == 1 or inserted == 3:
                checked = []
                index = 0
            insert_pattern()
            inserting = True

with open(sys.argv[1], "r") as file:
	contents = file.read()
	tokens = tokenizer.s_machine.get_tokens(contents)

php = grammar.Grammar()
php.load(php_grammar.table)
#php.serialize("grammar.ser")
#php = grammar.Grammar().deserialize("grammar.ser")
pattern_id = php.patterns + 1

print php.grammar

separator = 31
opening_tags = (108, 2, 3, 109, 5, 6)
closing_tags = (7, 110, 8)

nonterminal_id = 0
current_rule = 0
index = 0
inserting = False

stack = []
checked = []

instructions = 0
terminated = False
pattern = 0
trace = []

for item in tokens:
    token, lexeme, line = item[0], item[1], item[2]
    print "%s ========== %s %s ==========" % (line, token, lexeme)
    insert_pattern()
    if terminated:
        if not pattern == 0:
            instructions += 1
        terminated = False
        print "Pattern:", pattern, len(trace), trace
        pattern = 0
        trace = []
        print "End:", nonterminal_id, current_rule, token

print php.grammar
#php.serialize("grammar.ser")
print instructions
