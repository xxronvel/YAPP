import sys, tokenizer.s_machine, grammar

def get_expected_symbols():
    global nonterminal_id, index, queue, current_rule
    queue = php.grammar[nonterminal_id].get_expected_symbols(current_rule, index)

def parse():
    global nonterminal_id, index, current_rule, is_expected, queue, stack, token, move_down
    for expected in queue:
        #print "debug:", line, nonterminal_id, current_rule, index, expected[0], token
        if expected[0].is_terminal():
            if expected[0].token == token:
                index += 1
                is_expected = True
                move_down = True
                break
            else:
                current_rule += 1
                is_expected = False
        elif expected[0].is_nonterminal():
            stack.append((nonterminal_id, index, current_rule))
            nonterminal_id = expected[0].id
            index = 0
            current_rule = 0
            get_expected_symbols()
            parse()
            break
        else:
            if nonterminal_id != 0:
                last = stack.pop()
                nonterminal_id = last[0]
                if move_down and expected[1] < expected[2] - 1:
                    index = 0
                    current_rule = last[2] + 1
                else:
                    index = last[1] + 1
                    current_rule = last[2]
                get_expected_symbols()
                parse()
            break
    else:
        move_down = True
        index += 1
        current_rule += 1
        get_expected_symbols()
        parse()

def check_for_missing_tokens():
    global nonterminal_id, index, current_rule, is_expected, queue, stack, token
    for expected in queue:
        if expected[0].is_empty():
            if nonterminal_id != 0:
                last = stack.pop()
                nonterminal_id = last[0]
                index = last[1] + 1
                current_rule = last[2]
                get_expected_symbols()
                check_for_missing_tokens()
            break
        elif expected[0].is_nonterminal():
            stack.append((nonterminal_id, index, current_rule))
            nonterminal_id = expected[0].id
            index = 0
            current_rule = 0
            get_expected_symbols()
            check_for_missing_tokens()
            break
        else:
            print "Parse error, missing token on line %s" % (line)
            #print "Parse error, expected \"%s\" on line %s" % (expected[0], line)
            break

with open(sys.argv[1], "r") as file:
	contents = file.read()
	tokens = tokenizer.s_machine.get_tokens(contents)

php = grammar.Grammar()
php.read()

nonterminal_id = 0
current_rule = 0
index = 0
is_expected = True
move_down = False

queue = []
stack = []

for item in tokens:
    token = item[0]
    lexeme = item[1]
    line = item[2]
    get_expected_symbols()
    parse()
    if not is_expected:
        print "Parse error, unexpected \"%s\" on line %s" % (lexeme, line)
        break
else:
    token = 0
    get_expected_symbols()
    check_for_missing_tokens()
