'''
jsre provides a regular expression machine for efficiently searching large byte buffers.

Version 1.1.0

@author: Howard Chivers

Copyright (c) 2015, Howard Chivers
All rights reserved.
'''

from jsre.reobjects import compile, search, match, findall, finditer, purge
from jsre.reobjects import ReCompiler

from jsre.header import I, IGNORECASE, M, MULTILINE, S, DOTALL, X, VERBOSE, INDEXALT, SECTOR
from jsre.header import XDUMPPARSE
