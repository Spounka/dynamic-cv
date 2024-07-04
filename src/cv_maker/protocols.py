from pathlib import Path
from typing import Generator, List, Protocol, TypeVar, Generic, Dict, Any, Tuple

T = TypeVar("T", bound=Dict[str, Any], covariant=True)


class DataLoader(
    Generic[T],
    Protocol,
):
    def list_files(self, directory: Path) -> List[Path]: ...
    def parse_file(self, file: Path) -> dict[str, str] | None: ...
    def load_file(self, file: Path) -> Tuple[T | None, str]: ...
    def load_all_files_in_dir(
        self, path: Path
    ) -> Generator[Tuple[T, str], None, None]: ...


class BackendEngine(Protocol):
    def render(
        self, file: Path, output: str = "default", raise_on_exception: bool = False
    ): ...


class CvMakerMode(Protocol):
    def execute(self): ...
