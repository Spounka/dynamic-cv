import argparse
from pathlib import Path
from typing import Any, Generator, List, Protocol, Tuple

T = Any


class DataLoader(
    Protocol,
):
    def list_files(self, directory: Path) -> List[Path]: ...

    def parse_file(self, file: Path) -> T | None: ...

    def load_file(self, file: Path) -> Tuple[T | None, str]: ...

    def load_all_files_in_dir(
        self, path: Path
    ) -> Generator[Tuple[T, str], None, None]: ...


class BackendEngine(Protocol):
    def render(
        self, file: Path, output: str = "default", raise_on_exception: bool = False
    ): ...


class CvMakerMode(Protocol):
    def execute(self, data_loader: DataLoader, args: argparse.ArgumentParser): ...
