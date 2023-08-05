.DEFAULT_GOAL := all

all: test publish

test:
	python myFbase/myfbase.py

build:
	flit build

publish: build
	flit publish
