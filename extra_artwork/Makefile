# Griffith extra artwork makefile

# (c) 2005-2007 Vasco Nunes, Piotr Ozarowski

# $Id$


PACKAGE=griffith-extra-artwork
VERSION=0.9.3

.PHONY: help clean install

INSTALL ?= install
MAKE ?= make
RM ?= rm
FIND ?= find

PREFIX = $(DESTDIR)/usr
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/griffith/images

PYFILES := $(shell $(FIND) . -name "*.py" -print)

make: help

install: uninstall
	$(INSTALL) -m 755 -d $(DATADIR)
	$(INSTALL) -m 644 images/*.png $(DATADIR)
	
uninstall:
	${RM} -rf $(DATADIR)/PluginMovie*.png
	
clean:
	${RM} -f images/*.~
	
help:
	@echo Usage:
	@echo "make		- not used"
	@echo "make clean	- delete built modules and object files"
	@echo "make install	- install binaries into the official directories"
	@echo "make uninstall	- uninstall binaries from the official directories"
	@echo "make help	- prints this help"
	@echo "make dist	- makes a distribution tarball"
	@echo
	
dist: clean
	@tar --exclude=*.svn* --exclude=*.tar* --exclude=debian -cf temporary.tar ./
	@mkdir $(PACKAGE)-$(VERSION)
	@tar -xf temporary.tar -C $(PACKAGE)-$(VERSION)
	@${RM} temporary.tar
	@tar -czf $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION) && echo File ./$(PACKAGE)-$(VERSION).tar.gz generated successfully
	@${RM} -rf $(PACKAGE)-$(VERSION)
