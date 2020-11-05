from os.path import exists
import pathlib
from typing import Any

def read(path: str, **kwargs: Any) -> Any:
    filepath = pathlib.Path(path)
