#!/bin/bash
# Set present working directory
PWD="file://$(pwd)"

# Set cli variables
CREDENTIALS_FILE_PATH="credentials"

echo "AWS_DEFAULT_REGION=us-east-1" > $CREDENTIALS_FILE_PATH

# Bucket params and template
PARAMS_BUCKET_FILE_PATH="$PWD/IaC/params-artifacts-bucket.json"
TEMPLATE_BUCKET_FILE_PATH="$PWD/IaC/template-artifacts-bucket.yaml"
# Main params and template
PARAMS_MAIN_FILE_PATH="$PWD/IaC/params.json"
TEMPLATE_MAIN_FILE_PATH="$PWD/IaC/template.yaml"
# Stack Name variable
STACK_BUCKET_NAME="nu0087002eis-aid-dev-bucket-test-stack"
STACK_MAIN_NAME="nu0087002eis-aid-dev-main-test-stack"
# Update switch
UPDATE_SWITCH=${1:-"no"}
UPDATE_ARTIFACT=${2:-"si"}

# Now export all credentials aws variables to shell session
echo "Exporting aws credentials to shell session"
echo "credentials_file_path = $CREDENTIALS_FILE_PATH"

sleep 2

export $(grep -v '^#' $CREDENTIALS_FILE_PATH | xargs -0)

# Executing bucket stack first and wait until finish
if [[ $UPDATE_SWITCH == "no" ]]; then
    echo "creating mode stack"
    aws cloudformation create-stack --stack-name $STACK_BUCKET_NAME --template-body $TEMPLATE_BUCKET_FILE_PATH --parameters $PARAMS_BUCKET_FILE_PATH --capabilities CAPABILITY_IAM --on-failure DELETE
    # wait until finish
    aws cloudformation wait stack-create-complete --stack-name $STACK_BUCKET_NAME
    if [[ $UPDATE_ARTIFACT == "si" ]]; then
        # upload artifact to bucket
        aws s3 cp --recursive ./carta_laboral s3://nu0087002eis-aid-mlops-artifacts-bucket
        bash ./build_deploy_lambda.sh
    fi
    # create main stack
    aws cloudformation create-stack --stack-name $STACK_MAIN_NAME --template-body $TEMPLATE_MAIN_FILE_PATH --parameters $PARAMS_MAIN_FILE_PATH --capabilities CAPABILITY_NAMED_IAM --on-failure DELETE
elif [[ $UPDATE_SWITCH == "si" ]]; then
    echo "updating mode stack"
    # aws cloudformation update-stack --stack-name $STACK_BUCKET_NAME --template-body $TEMPLATE_BUCKET_FILE_PATH --parameters $PARAMS_BUCKET_FILE_PATH --capabilities CAPABILITY_IAM
    # wait until finish
    # aws cloudformation wait stack-update-complete --stack-name $STACK_BUCKET_NAME
    if [[ $UPDATE_ARTIFACT == "si" ]]; then
        # upload artifact to bucket
        # aws s3 cp --recursive ./carta_laboral s3://nu0087002eis-aid-mlops-artifacts-bucket
        bash ./build_deploy_lambda.sh
    fi
    aws cloudformation update-stack --stack-name $STACK_MAIN_NAME --template-body $TEMPLATE_MAIN_FILE_PATH --parameters $PARAMS_MAIN_FILE_PATH --capabilities CAPABILITY_NAMED_IAM
fi
