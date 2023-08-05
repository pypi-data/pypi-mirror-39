.PHONY: test
test:
	python2 setup.py test
	python3 setup.py test
	$(MAKE) test-sdist
	env PYTHONPATH=. python2 examples/hello_world.py
	env PYTHONPATH=. python3 examples/hello_world.py
	env PYTHONPATH=. python3 examples/dbc_io/main.py
	env PYTHONPATH=. python3 examples/diagnostics/did.py
	codespell -d $$(git ls-files | grep -v \.kcd | grep -v \.[hc])
	$(MAKE) test-c

.PHONY: test-c
test-c:
	gcc \
	    -Wall \
	    -Wpedantic \
	    -Werror \
	    -Wextra \
	    -std=c99 \
	    tests/main.c \
	    tests/files/c_source/motohawk.c \
	    tests/files/c_source/padding_bit_order.c \
	    tests/files/c_source/vehicle.c \
	    tests/files/c_source/multiplex.c \
	    tests/files/c_source/multiplex_2.c \
	    tests/files/c_source/floating_point.c \
	    tests/files/c_source/no_signals.c \
	    tests/files/c_source/choices.c && ./a.out

.PHONY: test-sdist
test-sdist:
	rm -rf dist
	python setup.py sdist
	cd dist && \
	mkdir test && \
	cd test && \
	tar xf ../*.tar.gz && \
	cd cantools-* && \
	python setup.py test

.PHONY: release-to-pypi
release-to-pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
