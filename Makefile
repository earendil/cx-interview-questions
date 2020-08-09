# Self-Documented Makefile
.DEFAULT_GOAL := help

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run_tests: ## [Runs the entire unit test suite.]
	@python3.8 -m unittest discover
