PYFILES := $(shell find -name '*.py')
LINTOPTS := --funcdoc --classdoc --changetypes --unreachable --privatevar

test: .lint .coverage

.lint: $(PYFILES)
	pychecker $(LINTOPTS) $*
	touch .lint

# Run the tests via coverage
.coverage: $(PYFILES)
	python -m coverage -x run_tests.py

show-coverage: .coverage
	python -m coverage -r -m -o /usr

clean:
	rm -f *.pyc **/*.pyc *.pyo **/*.pyo
	rm -f .lint .coverage
