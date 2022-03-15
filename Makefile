SHELL := /bin/bash
DEFAULT_GOAL := help
FILE_NAME := training

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docker-build:  ## Build the Docker image used in this project
	docker build . --progress tty -t udacity/mlops_tests_3:latest ;

bash:  ## Open an interactive terminal in Docker container
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm mlops

lint-with-pylint:  ## Lint library files. Can pass FILE_NAME name to lint.
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm -w /opt mlops \
	bash /root/project/scripts/linter-code.sh /root/project/src/$(FILE_NAME).py

lint-and-test:  ## Lint library files. Can pass FILE_NAME name to lint.
	docker-compose \
	-p mlops \
	-f docker-compose.yml \
	run --rm -w /root/project mlops \
	bash /root/project/scripts/linter-and-test.sh /root/project $(FILE_NAME)

test-modules:  ## Test modules implemented
	docker-compose \
	-p tests \
	-f docker-compose.yml \
	run --rm tests
