# $Id: Makefile 686 2007-01-07 22:36:07Z piotrek $
.PHONY: all man
MANPAGES= griffith.1

PREFIX= $(DESTDIR)/usr
MANDIR= $(PREFIX)/share/man
INSTALL ?= install
DOC2MAN ?= docbook2x-man

all: man

man: $(MANPAGES)

clean:
	$(RM) $(MANPAGES)

%.1: %.xml
	$(DOC2MAN) $<

install: $(MANPAGES)
	$(INSTALL) -m 755 -d "$(MANDIR)/man1"
	if test -n "$(MANPAGES)"; then $(INSTALL) -m 644 $(MANPAGES) $(MANDIR)/man1; fi

uninstall: $(MANPAGES)
	for manpage in $(MANPAGES); do \
		${RM} $(MANDIR)/man1/$$manpage; \
	done
