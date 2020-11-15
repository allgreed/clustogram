.DEFAULT_GOAL := help

# Porcelain
# ###############
.PHONY: env-up env-down env-recreate container run build lint test

run: setup ## run the app
	npm start

build: setup ## create artifact
	npm run build

lint: setup ## run static analysis
	npm run lint

test: setup ## run all tests
	npm test

# Plumbing
# ###############
.PHONY: setup

setup: node_modules

node_modules: package.json package-lock.json
	npm ci
	touch $@

# Helpers
# ###############
.PHONY:

# Utilities
# ###############
.PHONY: help todo clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: ## remove artifacts
	@# will remove everything in .gitignore expect for blocks starting with dep* or lib* comment
	@# TODO: add actual removal xD
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' testowy | grep '\S' | sort) <(awk '/^# *(dep|lib)/,/^$/' testowy | head -n -1 | tail -n +2 | sort) 

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
