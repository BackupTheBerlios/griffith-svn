# $Id$
LANGUAGES = en pl pt
DOC2MAN ?= docbook2x-man

.PHONY: man clean $(LANGUAGES) 


all: man

man: $(LANGUAGES)
	for dir in $(LANGUAGES); do \
	          $(MAKE) -C $$dir man; \
	done

clean: $(LANGUAGES)
	for dir in $(LANGUAGES); do \
	          $(MAKE) -C $$dir clean; \
	done

install:
	for dir in $(LANGUAGES); do \
	          $(MAKE) -C $$dir install; \
	done

uninstall:
	for dir in $(LANGUAGES); do \
	          $(MAKE) -C $$dir uninstall; \
	done
