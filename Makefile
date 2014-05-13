clean:
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	nosetests tests
