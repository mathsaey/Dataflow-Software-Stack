# run.py
# Mathijs Saey
# dvm prototype

import Queue

literals = Queue.Queue()

def main():
	while True:
		l = literals.get()
		l.activate()

def addLiteral(lit):
	literals.put(lit)