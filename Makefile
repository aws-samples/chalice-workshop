html:
	cd docs && make html
prcheck:
	flake8 code
