run:
	.venv/bin/python fetch.py
	g++ calc.cpp -o calc
	./calc
	.venv/bin/python plot.py
