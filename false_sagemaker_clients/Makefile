env_name := ./env
python_path := $(env_name)/bin/python3

init:
	conda create --prefix $(env_name)/ python=3.9 -y

dev:
	$(python_path) -m pip install -r requirements-dev.txt

test:
	$(python_path) -m pytest .

clean:
	rm -r $(env_name)