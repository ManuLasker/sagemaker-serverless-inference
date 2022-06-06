from pathlib import Path
from src.callbacks import validate_file_callback, validate_create_directory_callback
from src.lambda_controller import main as lambda_main

import typer

app = typer.Typer()

@app.command()
def call_lambda(
    lambda_name: str = typer.Argument("nu0087002eis-aid-dev-call-sagemaker-serverless-lambda",
                                      help="Name of the lambda to execute asynchronously"),
    false_clients_number: int = typer.Option(10, "-n",
                                             help="Number of false clients to create"),
    lambda_event_file_path: Path = typer.Option("inputs/lambda_event.json",
                                                "--event-file",
                                                help="Event json file to send",
                                                callback=validate_file_callback),
    result_directory_path: Path = typer.Option("results", 
                                               "--result-path",
                                               help="Results directory where to save"
                                               " the metadata for our test",
                                               callback=validate_create_directory_callback)
):
    lambda_main(false_clients_number, lambda_name,
                lambda_event_file_path, result_directory_path)

@app.command()
def call_sagemaker(
    sagemaker_endpoint_name: str = typer.Argument(..., 
                                                  help="Name of the sagemaker"
                                                  " endpoint to execute asynchronously"),
    false_clients_number: int = typer.Option(...,
                                             "-n",
                                             help="Number of false clients to create"),
    image_file_path: Path = typer.Option(..., "--image-file",
                                         help="Image input file to send", 
                                         callback=validate_file_callback)
):
    print("not implemented yet!")
    pass

if __name__ == "__main__":
    # run app
    app()