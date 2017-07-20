init:    
	virtualenv env
	env/bin/pip install -r requirements.txt
test:
	env/bin/nosetests --with-coverage -vs tests

.PHONY: init test
