from pathlib import Path
from typing import TypedDict, List, Tuple
import pytest
import yaml

from cv_maker.loader import YamlLoader


class MockLoadedDataType(TypedDict):
    name: str
    value: str


@pytest.fixture(scope="session")
def setup_data_loader():
    return YamlLoader[MockLoadedDataType]()


@pytest.fixture(scope="module")
def setup_temp_yml_files(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_files = [Path(temp_dir / f"file-{i}.yml").resolve() for i in range(5)]
    for f in temp_files:
        with open(f, "w", encoding="utf-8") as stream:
            yaml.dump({"name": "nazih", "value": "something"}, stream)
    return temp_dir, temp_files


@pytest.fixture(scope="module")
def setup_temp_mixed_files(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    temp_files = [
        Path(temp_dir / f"file-{i}.{'yml' if i % 2 == 0 else 'docx'}").resolve()
        for i in range(5)
    ]
    for f in temp_files:
        with open(f, "w", encoding="utf-8") as stream:
            yaml.dump({"name": "nazih", "value": "something"}, stream)
    return temp_dir, temp_files


def test_list_files_returns_all(setup_temp_yml_files, setup_data_loader):
    # assign
    temp_dir, temp_files = setup_temp_yml_files
    loader = setup_data_loader
    # act
    files = loader.list_files(temp_dir)
    # assert
    assert len(files) == len(temp_files)
    assert files == temp_files


def test_list_files_returns_only_yml(setup_temp_mixed_files, setup_data_loader):
    # assign
    temp_dir, temp_files = setup_temp_mixed_files
    loader = setup_data_loader
    # act
    files = loader.list_files(temp_dir)
    expected = list(filter(lambda x: x.suffix in [".yml", ".yaml"], temp_files))
    # assert
    assert len(files) == len(expected)
    assert set(files) == set(expected)  # set conversion to ensure unique files


def test_load_file_returns_name_and_data(
    setup_temp_yml_files: Tuple[Path, List[Path]],
    setup_data_loader: YamlLoader[MockLoadedDataType],
):
    # assign
    temp_dir, temp_files = setup_temp_yml_files
    loader: YamlLoader[MockLoadedDataType] = setup_data_loader
    # act
    loaded_data = list(loader.load_all_files_in_dir(temp_dir))
    # assert
    for (data, name), stream in zip(loaded_data, temp_files):
        assert name == stream.stem
        assert data == {"name": "nazih", "value": "something"}


def test_load_file_non_existent_raises(
    setup_data_loader: YamlLoader[MockLoadedDataType],
):
    # assign
    non_existent = Path("/tmp") / "non-existent.yml"
    loader: YamlLoader[MockLoadedDataType] = setup_data_loader
    # act
    # assert
    with pytest.raises(FileNotFoundError):
        loader.load_file(non_existent)


def test_load_file_bad_yaml_raises(
    setup_data_loader: YamlLoader[MockLoadedDataType],
):
    # assign
    non_existent = Path("/tmp") / "falty-existent.yml"
    with open(non_existent, "w", encoding="utf-8") as stream:
        yaml.dump({"name": "nazih", "value": "something"}, stream)
        stream.write("grabage=something")
    loader: YamlLoader[MockLoadedDataType] = setup_data_loader
    # act
    data, name = loader.load_file(non_existent)
    # assert
    assert data is None
    assert name == "falty-existent"
