PYFILES := $(shell echo **/*.py)
LINTOPTS := --funcdoc --classdoc --changetypes --unreachable --privatevar

test: .lint
	python -m rsyncconfig.test.__init__

.lint: $(PYFILES)
	pychecker $(LINTOPTS) $*
	touch .lint

clean:
	rm -f *.pyc **/*.pyc *.pyo **/*.pyo
	rm -f .lint
