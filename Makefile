PYTEST = py.test
# These targets are not files
.PHONY: coverage poetry test server install

##################
# Install commands
##################
install: ## Create a poetry env and install dev and production requirements
	poetry shell
	poetry install


##################
# Tests and checks
##################
test:## Run tests
	@poetry run $(PYTEST)

retest: ## Run failed tests only
	@poetry run $(PYTEST) --lf

coverage: ## Generate coverage report
	@poetry run $(PYTEST) --cov=api_consumer --cov-report=term-missing

##################
# Run flask dev server
##################
server:
	@poetry run python main.py
