from typing import Generator
from pathlib import Path
from typing import List, Any, TypeVar, Generic, Tuple, Dict

import yaml

T = TypeVar("T", bound=Dict[str, Any], covariant=True)


class YamlLoader(Generic[T]):
    def list_files(self, directory: Path) -> List[Path]:
        """Lists all yaml files in directory and returns them in a list"""
        return [
            file
            for file in directory.iterdir()
            if file.is_file() and file.suffix in [".yml", ".yaml"]
        ]

    def parse_file(self, file: Path) -> T | None:
        """Opens a yaml file and parses it"""
        try:
            with open(file, "r", encoding="utf-8") as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(err)
            return None

    def load_all_files_in_dir(self, path: Path) -> Generator[Tuple[T, str], None, None]:
        for file in self.list_files(path):
            data, name = self.load_file(file)
            if data:
                yield data, name

    def load_file(self, file: Path) -> Tuple[T | None, str]:
        data, name = (self.parse_file(file), file.name.split(".")[0])
        if not data:
            return None, name
        return (data, name)
