import os
import subprocess
from pathlib import Path
from typing import Generator, List, Literal, Tuple

import yaml
from jinja2 import Environment, FileSystemLoader, Template

import config
from cv_types import CVData, Language


def list_yaml_files(directory: Path) -> List[Path]:
    """Lists all yaml files in directory and returns them in a list"""
    return [
        file
        for file in directory.iterdir()
        if file.is_file() and file.suffix in [".yml", ".yaml"]
    ]


def load_yaml_file(file: Path):
    """Opens a yaml file and parses it"""
    try:
        with open(file, "r", encoding="utf-8") as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as err:
        print(err)
        return None


def load_data_files(path: Path) -> Generator[Tuple[CVData, str], None, None]:
    for file in list_yaml_files(path):
        data = load_yaml_file(file)
        if data:
            yield data, file.name.split(".")[0]


def render_template(template: Template, data: Language) -> str:
    """Renders a template with the data"""
    return template.render({**data, "image": PATH_TO_IMAGE})


def write_results_to_texfile(destination: str | Path, content: str) -> None:
    with open(destination, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    env = Environment(loader=FileSystemLoader(TEMPLATES))
    env.comment_start_string = "{#%"
    env.comment_end_string = "%#}"
    config.BUILD_DIR.mkdir(parents=True, exist_ok=True)

    for file, name in load_data_files(DATA_DIR):
        if not file["languages"]["en"]["summary"]["details"]:
            continue

        for lang in config.LANGS:
            data = file["languages"][lang]

            for form in config.FORMATS:
                temp = Path(config.BUILD_DIR / name / form / lang)
                temp.mkdir(parents=True, exist_ok=True)

                template = env.get_template(f"template_{form}.tex")
                result = render_template(template, data)

                write_results_to_texfile(temp / f"cv_{name}_{lang}_{form}.tex", result)
                os.chdir(temp)
                print(os.getcwd())

                print("\n\n\n-------------------------------------")
                print(f"Compiling CV_Nazih_Boudaakkar_{name} {lang} {form}")
                print("-------------------------------------\n\n\n")

                return_code = subprocess.run(
                    [
                        "xelatex",
                        f'--jobname="CV_Nazih_Boudaakkar_{name}"',
                        f"./cv_{name}_{lang}_{form}.tex",
                    ]
                )
                if return_code:
                    print("completed with return code ", return_code)


if __name__ == "__main__":
    main()
