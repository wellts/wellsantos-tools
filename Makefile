.PHONY: install
install:
	python3.10 -m venv .venv
	. .venv/bin/activate
	pip install poetry
	poetry install

.PHONY: coverage
coverage:
	APP_ENVIRONMENT=coverage poetry run pytest -n 6 --cov=wellsantos/ --cov-report=term-missing --cov-report=term:skip-covered --cov-report=xml ./tests/ --durations=5 -o log_cli=true --cov-config=.coveragerc --timeout=300

.PHONY: bandit
bandit:
	poetry run bandit -r -f custom wellsantos

.PHONY: mypy
mypy:
	poetry run mypy wellsantos --disable-error-code "annotation-unchecked" --disable-error-code "method-assign"

.PHONY: flake8
flake8:
	poetry run flake8 wellsantos tests

.PHONY: isort-check
isort-check:
	poetry run isort -c --profile=black -l 120 wellsantos tests

.PHONY: isort
isort:
	poetry run isort --profile=black -l 120 wellsantos tests

.PHONY: blue
blue:
	poetry run blue wellsantos tests

.PHONY: blue-check
blue-check:
	poetry run blue --check wellsantos tests

.PHONY: safety-check
safety-check:
	poetry run pip freeze | poetry run safety check --stdin

.PHONY: dead-fixtures
dead-fixtures:
	poetry run pytest -n auto --dead-fixtures

.PHONY: lint
lint: blue isort flake8 mypy bandit dead-fixtures

.PHONY: dev-lint-coverage
dev-lint-coverage: lint coverage
