PYFILES := $(shell find -name '*.py')
LINTOPTS := --funcdoc --classdoc --changetypes --unreachable --privatevar
COVERAGE_REPORT_FLAGS := --omit=/usr,tools/

## Tool binary locations
COVERAGE := tools/coverage
PYGENIE := tools/pygenie.py

test: .lint .coverage

## Internationalization ##
%.ui.h: %.ui
	intltool-extract --type=gettext/glade $<

## Testing and code metrics ##
.lint: $(PYFILES)
	pychecker $(LINTOPTS) $*
	touch .lint

# Run the tests via coverage
.coverage:
	@$(COVERAGE) run tools/run_tests.py

show-coverage: .coverage
	@$(COVERAGE) report -m $(COVERAGE_REPORT_FLAGS)

coverage-simple: .coverage
	@echo -n 'Total Coverage: '
	@$(COVERAGE) report -m $(COVERAGE_REPORT_FLAGS) | awk '/TOTAL/ {print $$4}'

complexity:
	@$(PYGENIE) complexity --verbose $(PYFILES)

complexity-avg:
	@echo -n 'Avg Complexity: '
	@echo 'scale=3;'$(shell make complexity | grep '^[MF] ' | awk '{s+=$$3} END {print s}')'/'$(shell make complexity | grep '^[MF] ' | awk '{print $$3}' | wc -l) | bc

cloc:
	@cloc --by-file --no3 --quiet $(PYFILES)

cloc-simple:
	@echo -n 'SLOC: '
	@cloc --no3 --quiet $(PYFILES) | awk '/SUM/ {print $$5}'

commentsmethod:
	@echo -n 'Avg Comments/Method: '
	@echo 'scale=3;'$(shell cloc --no3 --quiet --csv $(PYFILES) | awk -F, '/Python/ {print $$4}')'/'$(shell grep -r '^ *def*:*' './rsyncconfig/' | wc -l) | cat | bc

metrics: coverage-simple complexity-avg cloc-simple commentsmethod

metrics-full: show-coverage complexity cloc commentsmethod

clean:
	rm -f *.pyc **/*.pyc *.pyo **/*.pyo
	rm -f .lint .coverage
