#
# Installation
#

.PHONY: setup-tesseract
setup-tesseract:
	sudo add-apt-repository ppa:alex-p/tesseract-ocr5 -y
	sudo apt-get update
	sudo apt install -y tesseract-ocr
	sudo apt install tesseract-ocr-eng
	tesseract --version

.PHONY: setup
setup:
	pip install -U --no-cache-dir pip setuptools wheel poetry

.PHONY: install
install:
	poetry install --extras visualization

#
# linter/formatter/typecheck/testing
#

.PHONY: lint
lint: install
	poetry run ruff check --output-format=github .

.PHONY: format
format: install
	poetry run ruff format --check --diff .

.PHONY: typecheck
typecheck: install
	poetry run mypy --cache-dir=/dev/null .

#
# Testing
#

.PHONY: test
test:
	poetry run pytest
