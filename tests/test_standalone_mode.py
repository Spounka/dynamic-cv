import argparse
import os
from pathlib import Path
from typing import List, Tuple, Generator

import pytest
from cv_maker.mode import StandaloneMode
from cv_maker.protocols import BackendEngine, CvMakerMode, DataLoader


class MockEngine:
    def __init__(self):
        pass

    def render(
        self, file: Path, output: str = "default", raise_on_exception: bool = False
    ):
        pass


class MockDataLoader:
    def list_files(self, directory: Path) -> List[Path]:
        return [Path.cwd() for i in range(3)]

    def parse_file(self, file: Path) -> dict[str, str] | None:
        return {"placeholder": "data"}

    def load_file(self, file: Path) -> Tuple[dict[str, str] | None, str]:
        return ({"placeholder": "data"}, "filename")

    def load_all_files_in_dir(
        self, path: Path
    ) -> Generator[Tuple[dict[str, str], str], None, None]:
        yield ({"placeholder": "data"}, "filename")


class MockMode:
    def execute(self, data_loader: DataLoader, args: argparse.ArgumentParser) -> None:
        pass


@pytest.fixture
def setup_mock_engine() -> BackendEngine:
    return MockEngine()


@pytest.fixture
def setup_mock_mode() -> CvMakerMode:
    return MockMode()


@pytest.fixture
def setup_mock_data_loader() -> DataLoader:
    return MockDataLoader()


@pytest.mark.parametrize(
    "path",
    (("/tmp/something/nazih"), ("/tmp/output/nazih")),
)
def test_handle_output_directory_creates_parent(path):
    # Assign
    # Act
    output = StandaloneMode.handle_output_directory(path)

    # Assert
    assert output.parent.exists()
    assert output.exists() == False

    output.parent.rmdir()


@pytest.mark.parametrize(
    "path,expected",
    (
        ("/tmp/something/else", "/tmp/something/else"),
        ("/tmp/output/nazih", "/tmp/output/nazih"),
    ),
)
def test_handle_output_directory_returns_path(path, expected):
    # Assign
    # Act
    output = StandaloneMode.handle_output_directory(path)

    # Assert
    assert not output.exists()
    assert str(output.resolve()) == expected

    output.parent.rmdir()
