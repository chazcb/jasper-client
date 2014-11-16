install:
	pip install -r requirements/prod.txt
	pip install -r requirements/test.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	nosetests tests
