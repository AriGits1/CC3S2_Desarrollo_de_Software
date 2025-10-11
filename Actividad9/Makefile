VENV=.venv
PY=$(VENV)/bin/python3
PIP=$(VENV)/bin/pip
PYTEST=$(VENV)/bin/pytest

.PHONY: venv deps test_all test_unit cov clean

venv:
	python3 -m venv $(VENV)

deps: venv
	$(PIP) install -r requirements.txt

# Ejecuta pytest en cada sub-actividad
test_all: deps
	cd soluciones/aserciones_pruebas   && ../../$(PYTEST) -q || exit 1
	cd soluciones/pruebas_pytest       && ../../$(PYTEST) -q || exit 1
	cd soluciones/pruebas_fixtures     && ../../$(PYTEST) -q || exit 1
	cd soluciones/coverage_pruebas     && ../../$(PYTEST) --cov=models --cov-report term-missing -q || exit 1
	cd soluciones/factories_fakes      && ../../$(PYTEST) -q || exit 1
	cd soluciones/mocking_objetos      && ../../$(PYTEST) -q || exit 1
	cd soluciones/practica_tdd         && ../../$(PYTEST) -q || exit 1

test_unit:
	$(PYTEST) -m "unit" -q

cov:
	cd soluciones/coverage_pruebas && ../../$(PYTEST) --cov=models --cov-report term-missing -q

clean:
	rm -rf .venv .pytest_cache **/__pycache__ htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
