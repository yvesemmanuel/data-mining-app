install-dependencies:
	@pip install -r requirements.txt

install-dependencies-dev:
	@pip install -r requirements.dev.txt


install-all-dependencies:
	@make install-dependencies
	@make install-dependencies-dev

build:
	@make install-all-dependencies
	@python setup.py build

clean:
	@rm -rf ./build