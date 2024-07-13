import argparse
import os
from pathlib import Path
from typing import Union

from . import config
from .protocols import BackendEngine, DataLoader
from .template import Template


class StandaloneMode:
    def __init__(self, engine: BackendEngine, arg: argparse.ArgumentParser):
        self.parser = arg

        self.engine = engine
        self.template = Template(config.TEMPLATES)

    @staticmethod
    def validate_path(p: str, is_dir: bool = False, create: bool = False) -> Path:
        path = Path(p).resolve()
        if not is_dir and not path.exists():
            raise IOError(f"File {path.resolve()} does not exist")
        if is_dir and not path.is_dir():
            if create:
                path.mkdir(parents=True, exist_ok=True)
            else:
                raise IOError(f"{path.resolve()} is not a directory")
        return path

    @staticmethod
    def handle_output_directory(path: str) -> Path:
        out = Path(path).resolve()
        if not out.parent.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
        return out

    def __parse_arguments(self, arg: argparse.ArgumentParser):
        # workaround for the DAP-UI debugging problem
        # where filename gets passed twice

        import sys

        print(sys.argv[0], sys.argv[1])
        if sys.argv[0] == sys.argv[1] or Path(sys.argv[1]).resolve().exists():
            args = arg.parse_args(sys.argv[2:])
        else:
            args = arg.parse_args()

        template_file = self.validate_path(args.template, is_dir=False)
        data_file = self.validate_path(args.data, is_dir=False)
        out = self.handle_output_directory(args.out)
        return template_file, data_file, out

    @staticmethod
    def __write_content_to_file(destination: Union[str, Path], content: str) -> None:
        with open(destination, "w", encoding="utf-8") as file:
            file.write(content)

    def execute(self, data_loader: DataLoader, arg: argparse.ArgumentParser):
        template_file, data_file, out = self.__parse_arguments(arg)

        if not out.parent.is_dir():
            out.parent.mkdir(exist_ok=True, parents=True)

        os.chdir(out.parent.resolve())

        data, file_name = data_loader.load_file(data_file)
        if not data or not file_name:
            raise ValueError(f"Error in data file {data_file}")

        result = self.template.render(str(template_file.name), data["languages"][0])

        self.__write_content_to_file(out.parent / "output.tex", result)

        self.engine.render(
            out.parent / "output.tex", output=out.name, raise_on_exception=True
        )

    @staticmethod
    def init_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="CV Maker CLI")

        parser.add_argument(
            "--template",
            "-t",
            type=str,
            help="The template to use for building the CV",
            required=True,
        )

        parser.add_argument(
            "--data",
            "-f",
            type=str,
            help="The data YAML file to use for populating the CV",
            required=True,
        )

        parser.add_argument(
            "--out",
            "-o",
            type=str,
            help="The output directory, defaults to current directory",
            default=Path.cwd().resolve(),
        )

        return parser
