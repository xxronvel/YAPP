#!/usr/bin/python

import state_table, reserved

def get_event(input):
	try:
		if input.isalpha():
			key = "alpha"
		elif unicode(input).isnumeric():
			key = "numeric"
		else:
			key = input
	except UnicodeDecodeError:
		key = get_event(input.decode('unicode_escape'))
	return state_table.input.get(key, len(state_table.input))

def get_tokens(string):
	tokens = []
	next_state = lambda state, event : state_table.table[state][0][event]
	is_final = lambda state : state_table.table[state][1]
	token = lambda state : state_table.table[state][2]
	error = lambda state : state_table.table[state][3]
	error_message = lambda state : state_table.errors[state_table.table[state][3]]
	current_state = 0
	lexeme = ''
	index = 0
	count = 0
	checkpoint = 0
	line = 1
	new_lines = 0

	while index < len(string):
		char = string[index]
		if char == "\n":
			if current_state == 0:
				line += 1
			else:
				new_lines += 1
		event = get_event(char)
		#print "debug:", line, current_state, char, next_state(current_state, event)
		if next_state(current_state, event) > 0:
			current_state = next_state(current_state, event)
			index += 1
			lexeme += char
			checkpoint = current_state
		elif next_state(current_state, event) < 0:
			current_state = next_state(current_state, event)
			index += 1
			count += 1
		else:
			if current_state > 0:
				if is_final(current_state):
					tokens.append((reserved.words.get(lexeme, token(current_state)), lexeme, line))
				else:
					print "%s on line %s" % (error_message(current_state), line)
				current_state = 0
				lexeme = ''
				line += new_lines
				new_lines = 0
				if char.isspace():
					index += 1
			elif current_state < 0:
				if is_final(current_state):
					tokens.append((reserved.words.get(lexeme, token(checkpoint)), lexeme, line))
					lexeme = ''
				current_state = token(current_state)
				index -= count
				count = 0
				checkpoint = 0
				new_lines = 0
			else:
				if not char.isspace():
					tokens.append((reserved.words.get(char, None), char, line))
				index += 1
	if current_state > 0 and not is_final(current_state):
		print "%s on line %s" % (error_message(current_state), line)
	return tokens
