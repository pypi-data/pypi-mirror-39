all: clean build

build: 
	python setup.py build_ext --inplace

clean:
	python setup.py clean --all
	rm -f jppy/*.cpp
	rm -f -r build/
	rm -f jppy/*.so

dependencies:
	pip install -Ur requirements.txt

test:
	py.test

.PHONY: all clean build test dependencies
