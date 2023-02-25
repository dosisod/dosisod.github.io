all: test

test: ruff mypy black pytest refurb

ruff:
	ruff md2html test gen_index.py

mypy:
	mypy -p md2html
	mypy gen_index.py

black:
	black md2html test --check --diff --color -l 79

pytest:
	pytest

refurb:
	refurb md2html test
