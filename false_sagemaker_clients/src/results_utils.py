import csv
import json

from datetime import datetime
from pathlib import Path
from typing import Dict


COLUMNS = ["client_id", "status_response", "body_response",
           "elapsed_time", "current_date"]

def write_results(file_path: Path, metadata: Dict[str, str]):
    exist_file = True if file_path.exists() else False
    with open(file_path, 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        if not exist_file:
            csv_writer.writerow(COLUMNS)
        csv_writer.writerow(
           [metadata[col] for col in COLUMNS] 
        )