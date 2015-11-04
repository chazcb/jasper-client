install:
	pip install -r requirements/prod.txt
	pip install -r requirements/test.txt

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

integration:
	nosetests tests/integration --nocapture

unit:
	nosetests tests/unit --nocapture

test: unit integration
