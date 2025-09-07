BLK         =   black
MAKE        =   make
PIP         =   pip3

BASEDIR     =   $(CURDIR)
SRCDIR      =   ${BASEDIR}/rclogvis

help:
	@echo 'Makefile for rclogvis'
	@echo 'Usage:'
	@echo 'make black           reformat the code using black code formatter'
	@echo 'make clean           remove temporary files'
	@echo 'make install         install the package locally'
	@echo 'make uninstall       uninstall the package'

black:
	${BLK} *.py */*.py */*/*.py

clean:
	rm -f ${SRCDIR}/*.pyc
	rm -f ${SRCDIR}/apps/*.pyc

install:
	${MAKE} clean
	${MAKE} uninstall
	${PIP} install .
	${MAKE} clean

uninstall:
	${PIP} uninstall --yes rclogvis

.PHONY: help black clean install uninstall