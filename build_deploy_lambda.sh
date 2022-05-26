#! /bin/env bash

COMPONENT=call_sagemaker_lambda
S3_ARTIFACT_BUCKET_NAME=nu0087002ei-aid-mlops-artifacts-bucket

cd $COMPONENT
make prod

aws s3 cp $COMPONENT.zip s3://$S3_ARTIFACT_BUCKET_NAME/lambdas/$COMPONENT.zip

make clean
