.PHONY: help coverage linter mypy pre-commit test validate

help:
	@echo "  coverage   to source code coverage check"
	@echo "  help       to show this help"
	@echo "  linter     to static code analysis"
	@echo "  mypy       to static type checker"
	@echo "  pre-commit to source code validation"
	@echo "  test       to tests running"
	@echo "  validate   to source code validation"

coverage:
	tox -e coverage

linter:
	tox -e linter

setup:
	@echo "This function not implemented yet"

mypy:
	tox -e mypy

pre-commit:
	tox -e pre-commit

test:
	tox

validate:
	tox -e pre-commit; tox -e linter; tox -e mypy

build:
	tox -e build
