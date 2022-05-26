env_name := ./env
python_path := $(env_name)/bin/python3
lambda_zip := call_sagemaker_lambda.zip

init:
	conda create --prefix $(env_name)/ python=3.9 -y

dev:
	$(python_path) -m pip install -r requirements-dev.txt

test:
	$(python_path) -m pytest .

prod:
	echo "building requirements and packages"
	conda create --prefix $(env_name)/ python=3.9 -y
	$(python_path) -m pip install -r requirements.txt --target ./packages

	echo "building lambda package to be deployed on AWS"
	zip -r $(lambda_zip) src 
	zip -g $(lambda_zip) -r input
	zip -g $(lambda_zip) app.py
	zip -g $(lambda_zip) -r packages

clean:
	rm -r packages
	rm -r $(env_name)
	rm $(lambda_zip)