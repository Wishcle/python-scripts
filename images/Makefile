
.PHONY: all
all: sync

.PHONY: sync
sync:
	uv sync

.PHONY: test
test: lint check

.PHONY: lint
lint:
	uvx ruff check

.PHONY: fix
fix:
	uvx ruff check --fix

.PHONY: check
check:
	uvx ty check
