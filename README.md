# Sagemaker Serverless Inference

This repository contains infrastructure as code (Cloudformation templates) to deploy a serverless inference endpoint using AWS Sagemaker service. The Idea is to make a performance benchmark for this kind of endpoint and generate son results to see if it is a good strategy to deploy machine learning models.

# Underlying resources and infrastructure

The cloudformation templates will deploy the following resources on AWS.

[x] S3 Bucket to upload and save the model artifact and lambda zip </br>
[x] Lambda to test sagemaker endpoint </br>
[x] Lambda Execution Role with the necessary permissions</br>
[x] Sagemaker Execution Role with the necessary permissions</br>
[x] Sagemaker Model</br>
[x] Sagemaker Serverless Endpoint Config</br>
[x] Sagemaker Serverless Endpoint</br>

## How to use this repository

There are three important folders in this repository and one bash script that we need to execute:

- *IaC*: this folder contains all the cloudformation templates to deploy our test previous describe infrastructure.</br>
- *call_sagemaker_lambda*: this folder contains code for a lambda function, this will be upload to a s3 bucket and then deployed to aws using the cloudformation templates.</br>
- *false_sagemaker_clients*: this folder contains a cli app that for this case it will create any number of concurrent clients to the call_sagemaker lambda function and it will also generate a csv file with differents kind of metadata for our experimentation, for example the status response for each request, the actual response, the time take for the request to complete, and so on.

### Execute experiments

To execute an experiment first, we need an AWS Account an credentials already configured, and a `.tar.gz` model artifact to be deployed on AWS Sagemaker this need to be save in the current direcorty, for this case it is not parametrized so it will be located in a folder name `./carta_labolar/firma/v2/model.tar.gz`, then we simply execute the script `deploy.sh` as follows:

```Bash
./deploy.sh no si
```

This will first deploy the mlops artifacts bucket and wait until completion, then it will upload the model artifact and the lambda `.zip` file, to finally deploy the main resources for the whole application. After the deployment's completion tu run one experiments, execute the following commands:

```Bash
cd false_sagemaker_clients
make init
make dev
conda activate ./env/
python run.py call-lambda -n 180
```

This will generate 180 concurrent invocation to the lambda function and wait, then after completion it will generate a `.csv` file with data to analyze our experiment.

# Results

The results of the experiments and benchmark for this kind of model is the following:

## Serverless Endpoint:

Thanks to the serverless configuration the endpoint will not generate any cost if it not in used, the functionality is equal to a lambda function, the main factors are memory allocation and execution time:

![price_model](results/serverless_cost.png)

## Serverless Limits:

This kind of deployment have concurrent limits; however it is possible to configurate the client, in this case, the lambda function that will execute the sagemaker endpoint, with a `max_attemps` parameter in the retries configuration, in order to make as much retries as possible, the configuration is the following:

```Python
from botocore.config import Config
config = Config(
    read_timeout=900,
    connect_timeout=900,
    retries={
        "max_attempts": 100,
        "mode": "standard"
    }
)
```

with this configuration we can avoid to certain extend the ThrottleError for our client.

![endpoint_limits](results/serverless_limits.png)

## Without the max_attempts and with 10 more concurrent clients above the current limits

The current configuration limits for our serverless endpoint is 150 in `MaxConcurrency`, with this limits we create 160 concurrent false clients. These give the following result:

[150_without_max_attempts](false_sagemaker_clients/results/lambda_execution_05_26_2022_160.csv)

as you can see there are 10 clients with the following error:

```Text
{""errorMessage"": ""An error occurred (ThrottlingException) when calling the InvokeEndpoint operation (reached max retries: 0): None"", ""errorType"": ""ClientError"", ""requestId"": ""6cbb90ea-7d32-44d9-b363-31f5cd782fee"", ""stackTrace"": [""  File \""/var/task/app.py\"", line 21, in handler\n    response = sg.invoke_endpoint(\n"", ""  File \""/var/runtime/botocore/client.py\"", line 391, in _api_call\n    return self._make_api_call(operation_name, kwargs)\n"", ""  File \""/var/runtime/botocore/client.py\"", line 719, in _make_api_call\n    raise error_class(parsed_response, operation_name)\n""]}
```

## With the max_attempts and with 10 more concurrent clients above the current limits

The current configuration limits for our serverless endpoint is 150 in `MaxConcurrency`, with this limits we create 160 concurrent false clients; however in this case we use the `max_attempts` paramter. These give the following result:

[150_with_max_attempts](false_sagemaker_clients/results/lambda_execution_05_28_2022_160.csv)

As you can see in this case we don't have any errors, all our false concurrent clients are responding well and with the expected output prediction.

## More experimentation with false concurrent clients number up to 250

- [170_with_max_attempts](false_sagemaker_clients/results/lambda_execution_05_28_2022_170.csv)</br>
- [180_with_max_attempts](false_sagemaker_clients/results/lambda_execution_05_28_2022_180.csv)</br>
- [250_with_max_attempts](false_sagemaker_clients/results/lambda_execution_05_28_2022_250.csv)
