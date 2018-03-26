# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = PythonCitrinationClient
SOURCEDIR     = tmpsrc
BUILDDIR      = build
STATICDIR 	  = source

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

html: prepare
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)

prepare: clean
	mkdir $(SOURCEDIR)
	cp -a $(STATICDIR)/ $(SOURCEDIR)

apidoc: prepare
	sphinx-apidoc -f ../citrination_client -o $(SOURCEDIR)

gh-pages: html
	cd build/html && \
	git init && \
	git checkout -b gh-pages && \
	git add . && \
	git commit -m "updating sphinx" && \
	git remote add upstream git@github.com:CitrineInformatics/python-citrination-client.git && \
	git push upstream gh-pages --force