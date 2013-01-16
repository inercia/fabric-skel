

all: requirements

bin/python:
	virtualenv .

requirements: bin/python requirements.lst
	bin/pip install -r requirements.lst

clean:
	rm -rf bin build include lib local packages *.pyc



