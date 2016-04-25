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

words = {
#characters
	";" : 31,
	"(" : 32,
	")" : 33,
	"[" : 34,
	"]" : 35,
	"^" : 18,
	"~" : 27,
	"@" : 20,
	"{" : 36,
	"}" : 37,
	"," : 38,
	"\\": 127,
#words
	"True" : 10,
    "False" : 10,
    "Null" : 13,
    "and" : 23,
    "or" : 23,
    "xor" : 23,
	"abstract" : 40,
	"as" : 42,
	"break" : 43,
	"callable" : 44,
	"case" : 45,
	"catch" : 46,
	"class" : 47,
	"clone" : 48,
	"const" : 49,
	"continue" : 50,
	"declare" : 51,
	"default" : 52,
	"do" : 54,
	"echo" : 55,
	"else" : 56,
	"elseif" : 57,
	"enddeclare" : 59,
	"endfor" : 60,
	"endforeach" : 61,
	"endif" : 62,
	"endswitch" : 63,
	"endwhile" : 64,
	"extends" : 67,
	"final" : 68,
	"finally" : 69,
	"for" : 70,
	"foreach" : 71,
	"function" : 72,
	"global" : 73,
	"goto" : 74,
	"if" : 75,
	"implements" : 76,
	"include" : 77,
	"include_once" : 78,
	"instanceof" : 79,
	"insteadof" : 80,
	"interface" : 81,
	"namespace" : 84,
	"new" : 85,
	"print" : 86,
	"private" : 87,
	"protected" : 88,
	"public" : 89,
	"require" : 90,
	"require_once" : 91,
	"return" : 92,
	"static" : 93,
	"switch" : 94,
	"throw" : 95,
	"trait" : 96,
	"try" : 97,
	"use" : 99,
	"var" : 100,
	"while" : 101,
	"yield" : 102,
#tags
	"<?php" : 108,
	"<script language=\"php\">" : 109,
	"</script>" : 110,
#variables
	"$GLOBALS" : 111,
	"$_SERVER" : 112,
	"$_GET" : 113,
	"$_POST" : 114,
	"$_FILES" : 115,
	"$_REQUEST" : 116,
	"$_SESSION" : 117,
	"$_ENV" : 118,
	"$_COOKIE" : 119,
	"$php_errormsg" : 120,
	"$HTTP_RAW_POST_DATA" : 121,
	"$http_response_header" : 122,
	"$argc" : 123,
	"$argv" : 124,
#functions
	"__halt_compiler" : 39,
	"array" : 41,
	"die" : 53,
	"empty" : 58,
	"eval" : 65,
	"exit" : 66,
	"isset" : 82,
	"list" : 83,
	"unset" : 98,
	"gzinflate" : 128,
	"str_rot13" : 129,
	"str_replace" : 130,
	"base64_decode" : 131,
	"escapeshellarg" : 132,
	"escapeshellcmd" : 133,
	"exec" : 134,
	"passthru" : 135,
	"proc_​close" : 136,
	"proc_​get_​status" : 137,
	"proc_​nice" : 138,
	"proc_​open" : 139,
	"proc_​terminate" : 140,
	"shell_​exec" : 141,
	"system" : 142,
	"preg_replace" : 143,
	"gzuncompress" : 144,
}
