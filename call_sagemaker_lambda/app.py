import json
import sys
import boto3
import os
from PIL import Image
from botocore.config import Config
from src.utils.image_utilities import pil_to_base64 

config = Config(
    read_timeout=900,
    connect_timeout=900,
    retries={"max_attempts": 0}
)

sg = boto3.client("sagemaker-runtime", region_name="us-east-1", config=config)

def handler(event, context = None):
    with Image.open(event.get("input_image_path", "input/carta_laboral_firma.jpg")) as pil_image:
        base64_im = pil_to_base64(pil_image)
        # Make serverless prediction
        response = sg.invoke_endpoint(
            EndpointName = event["endpoint_name"],
            Body = json.dumps(base64_im).encode(),
            ContentType = "application/json"
        )
        return json.loads(response['Body'].read().decode())

if __name__ == "__main__":
    print("Make a call to a sagemaker serverless endpoint")
    result = handler({
        "endpoint_name": "nu0087002ei-aid-dev-firma-model",
        "input_image_path": sys.argv[1]
    })
    print(result)