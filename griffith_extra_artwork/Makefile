# Griffith extra artwork makefile

# (c) 2005 Vasco Nunes
#

# $Id: Makefile,v 1.1.1.1 2005/10/01 12:14:37 iznogoud Exp $


PACKAGE=griffith_extra_artwork
VERSION=0.5.1

.PHONY: help clean install

PYTHON ?= python2.3
INSTALL ?= install
MAKE ?= make
RM ?= rm
MSGFMT ?= msgfmt
MSGMERGE ?= msgmerge
XGETTEXT ?= xgettext
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
	${RM} -f *.pyc *.bak images/*.~
	
help:
	@echo Usage:
	@echo "make		- not used"
	@echo "make clean	- delete built modules and object files"
	@echo "make install	- install binaries into the official directories"
	@echo "make uninstall	- uninstall binaries from the official directories"
	@echo "make help	- prints this help"
	@echo "make dist	- makes a distribution tarball"
	@echo "make package	- makes a Debian package"
	@echo
	
dist:
	@tar --exclude=*.svn* --exclude=*.tar* -cf griffith_extra_artwork.tar ./
	@mkdir $(PACKAGE)-$(VERSION)
	@tar -xf griffith_extra_artwork.tar -C $(PACKAGE)-$(VERSION)
	@${RM} griffith_extra_artwork.tar
	@tar -czf $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION) && echo File ./$(PACKAGE)-$(VERSION).tar.gz generated successfully
	@${RM} -rf $(PACKAGE)-$(VERSION)

package:
	@echo "Remember to update the debian/changelog file!"
	dpkg-buildpackage -rfakeroot
