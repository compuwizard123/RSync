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

complexity-avg:
	@echo 'Avg complexity'
	@echo 'scale=3;'$(shell make complexity | grep '^[MF] ' | awk '{s+=$$3} END {print s}')'/'$(shell make complexity | grep '^[MF] ' | awk '{print $$3}' | wc -l) | bc
cloc:
	cloc --by-file-by-lang --no3 --quiet $(PYFILES)

commentsmethod:
	@echo 'Avg Comments/Method'
	@echo 'scale=3;'$(shell cloc --no3 --quiet --csv $(PYFILES) | awk -F, '/Python/ {print $$4}')'/'$(shell grep -r '^ *def*:*' ./rsyncconfig/ | wc -l) | cat | bc

metrics: complexity-avg show-coverage cloc commentsmethod

clean:
	rm -f *.pyc **/*.pyc *.pyo **/*.pyo
	rm -f .lint .coverage
