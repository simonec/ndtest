init:
	virtualenv env
	env/bin/pip install -r requirements.txt
test:
	env/bin/coverage run --source=ndtest.model,ndtest.loader,ndtest.inspection -m nose -vs
	env/bin/coverage report --show-missing

install:
	env/bin/python setup.py install

develop:
	env/bin/python setup.py develop
