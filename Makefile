PYFILES := $(shell find -name '*.py')
LINTOPTS := --funcdoc --classdoc --changetypes --unreachable --privatevar

test: .lint .coverage

.lint: $(PYFILES)
	pychecker $(LINTOPTS) $*
	touch .lint

# Run the tests via coverage
.coverage:
	#python -m coverage -x run_tests.py
	coverage -x run_tests.py

show-coverage: .coverage
	#python -m coverage -r -m -o /usr
	coverage -r -m -o /usr

complexity:
	./pygenie.py complexity --verbose $(PYFILES)

complexity-simple:
	./pygenie.py complexity $(PYFILES)
cloc:
	cloc --by-file-by-lang --no3 --quiet $(PYFILES)

metrics: complexity show-coverage cloc

clean:
	rm -f *.pyc **/*.pyc *.pyo **/*.pyo
	rm -f .lint .coverage
