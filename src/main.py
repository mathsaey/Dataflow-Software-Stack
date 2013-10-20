# main.py
# Mathijs Saey
# dvm prototype

import if1parser.parser
import core.runtime

#loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/sort.if1"
loc = "/Users/mathsaey/Documents/Vub/Thesis/Repo/examples/simple.if1"

if1parser.parser.parseFile(loc)
core.runtime.main.run()