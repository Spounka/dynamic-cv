from pathlib import Path
from typing import Any, Generator, List, Protocol


class DataLoader(Protocol):
    def list_files(self, directory: Path) -> List[Path]: ...
    def load_file(self, file: Path) -> dict | None: ...
    def load_all_files_in_dir(self, path: Path) -> Generator[Any, None, None]: ...


class BackendEngine(Protocol):
    def render(
        self, file: Path, output: str = "default", raise_on_exception: bool = False
    ): ...


class CvMakerMode(Protocol):
    def execute(self): ...
