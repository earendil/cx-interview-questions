# Self-Documented Makefile
.DEFAULT_GOAL := help

.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run_tests: ## [Runs the entire unit test suite.]
	@python3.8 -m unittest discover

run_example_one:  ## [Runs only the example one test.]
	@python3.8 -m unittest tests.test_pricer.TestBasketPricer.test_assignment_example_one

run_example_two:  ## [Runs only the example two test.]
	@python3.8 -m unittest tests.test_pricer.TestBasketPricer.test_assignment_example_two
