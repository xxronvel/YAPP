#!/usr/bin/python
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

import argparse, sqlite3, pickle, random, sys

from os import path
from glob import glob
from tokenizer import s_machine
from parser import php_grammar, grammar, inserter, parser
from subprocess import Popen, PIPE
from string import ascii_letters

examples = """
Examples:
./yapp.py foo.php
./yapp.py -R /var/www/
./yapp.py -r 404.php --desc "Backdoor file" foo.php
"""

database = 'yapp.db'
grammar_source = 'grammar.ser'

def insert_pattern(pattern_id, description, instructions, tokens):
    result = False
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute("insert into Pattern values (:id, :desc, :instructions, :tokens);",
                        {"id" : pattern_id,
                         "desc" : description,
                         "instructions" : instructions,
                         "tokens" : sqlite3.Binary(pickle.dumps(tokens))});
        connection.commit()
        result = True
    except sqlite3.Error, e:
        if connection:
            connection.rollback()
        print "Error: {}".format(e.args[0])
        result = False
    finally:
        if connection:
            connection.close()
    return result

def select_pattern(pattern_id):
    result = None
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('select description, instructions from Pattern where id = ?', (pattern_id,))
        result = cursor.fetchone()
    except sqlite3.Error, e:
        print "Error: {}".format(e.args[0])
    finally:
        if connection:
            connection.close()
    return result

def select_all_pattern():
    result = None
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('select id, description from Pattern')
        header = True
        for pattern in cursor.fetchall():
            if header:
                print "ID\tDESCRIPTION"
                header = False
            print "{}\t{}".format(pattern[0], pattern[1])
        if header:
            print "Patterns not found"

    except sqlite3.Error, e:
        print "Error: {}".format(e.args[0])
    finally:
        if connection:
            connection.close()
    return result

def delete_pattern(pattern_id, verbose):
    result = True
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('select id from Pattern where id = ?', (pattern_id,))
        if cursor.fetchone():
            cursor.execute('select description, contents from Pattern where id != ?', (pattern_id,))
            result_set = cursor.fetchall()
            cursor.execute('delete from Pattern')
            connection.commit()

            php = grammar.Grammar()
            php.load(php_grammar.table)

            for pattern in result_set:
                description = pattern[0]
                tokens = pickle.loads(pattern[1])
                ins = inserter.Inserter(php, verbose)
                ins.run(tokens)
                php = ins.grammar
                if not insert_pattern(ins.pattern_id, description, ins.instructions, tokens):
                    result = False
            php.serialize(grammar_source)
        else:
            result = False
            print "Pattern not found"

    except sqlite3.Error, e:
        print "Error: {}".format(e.args[0])
        result = False
    finally:
        if connection:
            connection.close()
    return result

def reset():
    result = True
    grammar_ = grammar.Grammar()
    grammar_.load(php_grammar.table)
    grammar_.serialize(grammar_source)
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        cursor.execute('delete from Pattern')
        connection.commit()
    except sqlite3.Error, e:
        print "Error: {}".format(e.args[0])
        result = False
    finally:
        if connection:
            connection.close()
    return grammar_, result

def list_dir(directory, recursive):
    files = []
    contents = glob("{}/*".format(directory))
    for entry in contents:
        if path.isdir(entry):
            if recursive:
                files += list_dir(entry, recursive)
        elif path.isfile(entry):
            files.append(entry)
    return files

def decode(file_name, script, snippets, decoded_dir):
    print "Decoding obfuscated PHP code..."
    script += "\n<?php\n"

    var = ''.join(random.SystemRandom().choice(ascii_letters) for _ in range(10))

    name, ext = path.splitext(file_name)

    outputs = []

    for snippet in snippets:
        code, line = snippet
        output = '{}/{}_line_{}{}'.format(decoded_dir, name, line, ext)
        outputs.append(output)
        script += "${} = fopen('{}', 'w');\n".format(var, output)
        script += "fwrite(${}, {});\n".format(var, code)
        script += "fclose(${});\n".format(var)
    script += "?>"

    p = Popen("php", stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    p.stdin.write(script)
    stdout, stderr = p.communicate()

    header = True
    for out in outputs:
        if path.isfile(out):
            if header:
                print "Decoded strings were written to: "
                header = False
            print "{}".format(out)
    if header:
        print "Sorry, something went wrong"

def main():
    args_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                          description='Yet Another PHP Parser\nSearch patterns in PHP files using a parser',
                                          epilog=examples
                                          )
    args_parser.add_argument('-v', '--verbose', dest="verbose", action="count", default=0,
                        help='increase output verbosity')
    args_parser.add_argument('-l', '--list', dest="list", action='store_true',
                        help='list patterns')
    delete_args = args_parser.add_mutually_exclusive_group()
    delete_args.add_argument('--del', dest="delete", type=int, metavar='ID',
                        help='delete pattern')
    delete_args.add_argument('--reset', dest="reset", action='store_true',
                        help='reset the grammar')
    parser_args = args_parser.add_argument_group('Parser', 'Search patterns in files')
    inserter_args = args_parser.add_argument_group('Inserter', 'Insert pattern from file')
    parser_args.add_argument('input', nargs='*', type=str, metavar='INPUT',
                        help='input file or directory')
    parser_args.add_argument('-R', '--recursive', dest='recursive', action='store_true',
                        help='parse subdirectories recursively')
    parser_args.add_argument('--decode', dest="decode", action='store_true',
                        help='decode obfuscated PHP code')
    parser_args.add_argument('--dir', dest="directory", type=str, metavar='DIRECTORY', default='.',
                        help='write decoded files into DIRECTORY (default \'.\')')
    inserter_args.add_argument('-r', '--read', dest='read', type=str, metavar='FILE',
                        help="read pattern from FILE (requires that --desc also be set)")
    inserter_args.add_argument('--desc', dest="description", metavar='DESC',
                        help='description of the pattern to be read')
    inserter_args.add_argument('-i', '--insert', dest='insert', action='store_true',
                        help="insert pattern into grammar (requires that -r and --desc also be set)")
    args = args_parser.parse_args()

    verbose = args.verbose

    if args.list:
        select_all_pattern()

    if not args.reset:
        php = grammar.Grammar().deserialize(grammar_source)
    else:
        php, result = reset()
        if result:
            print "Done"

    if args.delete:
        if delete_pattern(args.delete, verbose):
            print "Pattern deleted"

    if args.directory:
        if path.isdir(args.directory):
            decoded_dir = args.directory
        else:
            args_parser.error("Cannot access {}: No such file or directory".format(args.directory))

    if args.read:
        if args.description:
            try:
                with open(args.read, 'r') as file_obj:
                    print "Reading pattern from {}...".format(file_obj.name)
                    contents = file_obj.read()
                    tokens, result = s_machine.get_tokens(contents, verbose)
                    if result:
                        ins = inserter.Inserter(php, verbose)
                        ins.run([token[0] for token in tokens])
                        php = ins.grammar
                        if ins.instructions > 0:
                            if args.insert:
                                if insert_pattern(ins.pattern_id, args.description, ins.instructions, [token[0] for token in tokens]):
                                    php.serialize(grammar_source)
                                    print "Pattern inserted"
                            else:
                                print "Done"
                        else:
                            print "Pattern exists. Nothing to do"
                    else:
                        print "Cannot parse {}: This file contains embedded code which does not allow forming PHP tokens".format(file_obj.name)
            except IOError:
                print "Cannot access {}: No such file or directory".format(args.read)
        else:
            args_parser.error("argument --desc is required")

    files = []
    for name in args.input:
        if path.isdir(name):
            files += list_dir(name, args.recursive)
        else:
            files.append(name)

    for name in files:
        try:
            with open(name, 'r') as file_obj:
                print "Parsing {}...".format(file_obj.name)
                contents = file_obj.read()
                tokens, result = s_machine.get_tokens(contents, verbose)
                if result:
                    par = parser.Parser(php, verbose)
                    if par.run(tokens):
                        if len(par.patterns) == 0:
                            print "No matches found"
                        else:
                            for pattern in par.patterns:
                                result = select_pattern(pattern)
                                if result:
                                    description, instructions = result
                                    if par.instructions[pattern] == instructions:
                                        print description
                                else:
                                    if args.description:
                                        print args.description
                                    else:
                                        print "Description not available"
                            if args.decode and len(par.snippets) > 0:
                                if tokens[-1][0] not in php_grammar.closing_tags:
                                    par.script += '\n?>'
                                decode(path.basename(file_obj.name), par.script, par.snippets, decoded_dir)
                else:
                    print "Cannot parse {}: This file contains embedded code which does not allow forming PHP tokens".format(file_obj.name)
        except IOError:
            print "Cannot access {}: No such file or directory".format(name)

if __name__ == "__main__":
    main()
