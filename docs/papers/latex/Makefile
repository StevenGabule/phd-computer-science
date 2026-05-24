# CiteCheck paper — common LaTeX build commands.
# Requires latexmk + a TeX distribution (TeX Live recommended).

PAPER ?= main

.PHONY: pdf watch clean wordcount help

help: ## Show this help
	@echo "CiteCheck paper build:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

pdf: ## Build the PDF
	latexmk -pdf -interaction=nonstopmode $(PAPER).tex

watch: ## Auto-rebuild on save (latexmk preview-continuous)
	latexmk -pdf -pvc -interaction=nonstopmode $(PAPER).tex

clean: ## Remove all build artifacts
	latexmk -C
	rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).run.xml

wordcount: ## Word count (approximate — uses texcount)
	@texcount -inc -1 -sum $(PAPER).tex 2>/dev/null || echo "texcount not installed (apt install texlive-extra-utils or brew install texcount)"
