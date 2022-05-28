import boto3
import time

from datetime import datetime
from uuid import uuid4
from botocore.config import Config

from typing import BinaryIO, TextIO, IO, Union
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from src.results_utils import write_results


FILE_NAME = '{execution_type}_{date_string}_{n_clients}.csv'

config = Config(
    read_timeout=900,
    connect_timeout=900,
    retries={"max_attempts": 100}
)
lambda_client = boto3.client('lambda', config=config)

def call_lambda(execution_number: int, call_identifier: int, lambda_name: str,
                payload: Union[bytes, IO, TextIO, BinaryIO],
                file_path: Path, current_date: str):

    try:
        print(f'Executing lambda function: {lambda_name}'
              f' with call identifier: {call_identifier}')
        init_time = time.time()
        response = lambda_client.invoke(
            FunctionName = lambda_name,
            Payload = payload,
            # InvocationType = 'Event'
        )
        # get metadata values
        elapsed_time = time.time() - init_time
        status = response['StatusCode']
        body_response = response['Payload'].read().decode()
        print(f'response payload: {body_response}'
              f' for call_identifier: {call_identifier}')
    except Exception as error:
        msg = ("There was a problem when invoking lambda function "
              f"{lambda_name}, error: {error}")
        print(msg)
        # get metdata values
        body_response = msg
        status = 500
        elapsed_time = 0

    write_results(file_path, metadata={"execution_number": execution_number,
                                       "client_id": call_identifier,
                                       "status_response": status,
                                       "body_response": body_response,
                                       "elapsed_time": elapsed_time,
                                       "current_date": current_date})

def main(n_clients: int, lambda_name: str,
               lambda_event_file_path: Path, result_path: Path):
    current_date = datetime.now().strftime("%m_%d_%Y")
    file_path = result_path / FILE_NAME.format(execution_type="lambda_execution",
                                            date_string=current_date,
                                            n_clients=n_clients)
    args = [(i, str(uuid4()), lambda_name,
             lambda_event_file_path.read_bytes(),
             file_path, current_date)
            for i in range(n_clients)]
    args = list(zip(*args))
    init_time = time.time()
    with ThreadPoolExecutor(max_workers=n_clients) as executor:
        executor.map(call_lambda, *args, timeout=900)
    total_time = time.time() - init_time
    print(f'total execution time was {total_time:0.2f}s')