all: test

test: typos ruff mypy black pytest refurb

typos:
	typos --format brief

ruff:
	ruff md2html test gen_index.py

mypy:
	mypy -p md2html
	mypy -p test
	mypy gen_index.py

black:
	black md2html test --check --diff --color -l 79

pytest:
	pytest

refurb:
	refurb md2html test

clean:
	rm -rf .mypy_cache .ruff_cache .pytest_cache .coverage
