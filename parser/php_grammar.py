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

table = {
    0 : ((108, -7, -1),
         (2, -7, -1),
         (3, -7, -1),
         (109, -7, -3),
         (5, -7, -5),
         (6, -7, -5)),
    1 : ((7, ),
         (31, -2),
         (72, 15, 32, -14, 33, 36, -23, 37, -2),
         (-24, -25)),
    25: ((7, ),
         (31, -2)),
    2 : ((7, ),
         (-7, -1),
         ()),
    3 : ((110, ),
         (31, -4),
         (72, 15, 32, -14, 33, 36, -23, 37, -4),
         (-24, -26)),
    26: ((110, ),
         (31, -4)),
    4 : ((110, ),
         (-7, -3),
         ()),
    5 : ((8, ),
         (31, -6),
         (72, 15, 32, -14, 33, 36, -23, 37, -6),
         (-24, -27)),
    27: ((8, ),
         (31, -6)),
    6 : ((8, ),
         (-7, -5),
         ()),
    23: ((72, 15, 32, -14, 33, 36, -23, 37),
         (-9, 31, -23),
         (92, -9, 31),
         ()),
    7 : ((49, 15, 106, -8),
         (-9, ),
         ()),
    8 : ((11, ),
         (12, ),
         (10, ),
         (34, -12, 35),
         (41, 32, -12, 33)),
    9 : ((11, -11),
         (12, -19),
         (10, -11),
         (34, -14, 35, -11),
         (41, 32, -14, 33, -11),
         (85, 15, 32, 33, -11),
         (32, -9, 33, -11),
         (15, 32, -14, 33, -11),
         (14, -20),
         (22, 14, -11)),
    10: ((22, ),
         (-17, ),
         (32, -14, 33),
         ()),
    11: ((19, -9),
         (30, -9),
         (105, -9, 107, -9),
         ()),
    12: ((-8, -13), ),
    13: ((38, -8, -13),
         ()),
    14: ((-9, -15),
         (125, 14, -15),
         ()),
    15: ((38, -16),
         ()),
    16: ((-9, -15),
         (125, 14, -15)),
    17: ((106, -18),
         (17, -9)),
    18: ((-9, ),
         (125, 14)),
    19: ((28, -21),
         (-11, )),
    20: ((28, -21),
         (-10, -11)),
    21: ((14, -22),
         (15, -22),
         (12, -22)),
    22: ((28, -21),
         ()),
    24: ()
}

separator = 31

opening_tags = (108, 2, 3, 109, 5, 6)

closing_tags = (7, 110, 8)

string_functions = (128, 129, 130, 131, 143, 144)

assignment_operators = (17, 106)

brackets = (34, 35)

curly_brackets = (36, 37)

round_brackets = (32, 33)

ignored_tokens = (127, 26, 20)
