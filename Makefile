PYFILES := $(shell find rsyncconfig/ -name '*.py') bin/rsyncconfig
UIFILES := $(shell find data/ui/ -name '*.ui')
LINTOPTS := --funcdoc --classdoc --changetypes --unreachable --privatevar
COVERAGE_REPORT_FLAGS := --omit=/usr,tools/

## Tool binary locations
COVERAGE := tools/coverage
PYGENIE := tools/pygenie.py

default: test

## Internationalization ##
LANGS := en_US es
POTFILE := data/locale/messages.pot
POFILES := $(foreach lang,$(LANGS),data/locale/$(lang).po)
MOFILES := $(POFILES:%.po=%/LC_MESSAGES/rsyncconfig.mo)

i18n: $(POTFILE) $(POFILES) $(MOFILES)

# Generate the template .pot file
$(POTFILE): $(PYFILES) $(UIFILES:%.ui=%.ui.h)
	mkdir -p $(dir $@)
	xgettext -k_ -kN_ -o $@ $^

# Create or update a .po file for a language
%.po: $(POTFILE)
	( if [ -f $@ ] ; then \
	    msgmerge -U $@ $< ; \
	  else \
	    msginit -i $< -o $@ --no-translator --locale $(basename $(notdir $@)) ; \
	  fi )

# Compile .po files into .mo binary files
%/LC_MESSAGES/rsyncconfig.mo: %.po
	mkdir -p $(dir $@)
	msgfmt $< -o $@

%.ui.h: %.ui
	intltool-extract --type=gettext/glade $<

## Testing and code metrics ##
test: .lint .coverage

.lint: $(PYFILES)
	pychecker $(LINTOPTS) $*
	touch .lint

# Run the tests via coverage
.coverage: $(PYFILES) $(MOFILES)
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
	rm -f $(MOFILES) data/ui/*.ui.h
