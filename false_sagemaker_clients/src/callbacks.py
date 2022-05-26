import os
from pathlib import Path
from typing import Optional
from gettext import gettext as _
from click.exceptions import ClickException, FileError

class IsNotDirectoryError(ClickException):
    """Raised if a path is not a directory"""
    def __init__(self, directoryname: str, hint: Optional[str] = None) -> None:
        if hint is None:
            hint = _("unknown error")

        super().__init__(hint)
        self.ui_filename = os.fsdecode(directoryname)
        self.filename = directoryname

    def format_message(self) -> str:
        return ("Provided path is not a directory {filename!r}: {message}").format(
            filename=self.ui_filename, message=self.message
        ) 

def validate_file_callback(value: Path):
    if not value.exists():
        raise FileError(value, hint=f'the file, {value}, does not exist')
    return value

def validate_create_directory_callback(value: Path):
    if value.is_dir() or not value.exists():
        value.mkdir(exist_ok=True)
    else:
        raise  IsNotDirectoryError(value,
                                   hint=f'the path, {value}, must be a directory'
                                        ', if the path passed is intended to be'
                                        ' a directory, but does not exist, '
                                        'it will be created automatically')
    return value