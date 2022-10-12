CONTAINER_NAME=atomic-red-team-client
CONTAINER_REGISTRY ?= localhost:5000

all: clean build

clean:
	rm -rf dist

app: install

build:
	poetry build

install:
	poetry install

update:
	poetry show -o
	poetry update
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	poetry show --tree

test:
	poetry run coverage run -m pytest --durations=0

coverage:
	poetry run coverage json -o coverage/json/coverage.json --pretty-print
	poetry run coverage html -d coverage/html

release: build
	poetry publish

container: build-container

build-container:
	docker build -t $(CONTAINER_REGISTRY)/$(CONTAINER_NAME) .

export-container:
	docker save $(CONTAINER_NAME) | gzip > $(CONTAINER_NAME).tar.gz

release-container:
	docker push $(CONTAINER_REGISTRY)/$(CONTAINER_NAME)
