import os
import subprocess
from pathlib import Path

import config

from template import Template
from loader import YamlLoader
from protocols import DataLoader


def write_results_to_texfile(destination: str | Path, content: str) -> None:
    with open(destination, "w", encoding="utf-8") as file:
        file.write(content)


def main():
    config.BUILD_DIR.mkdir(parents=True, exist_ok=True)

    dataLoader: DataLoader = YamlLoader()

    template = Template(config.TEMPLATES)

    for file, name in dataLoader.load_all_files_in_dir(config.DATA_DIR):
        if not file["languages"]["en"]["summary"]["details"]:
            continue

        for lang in config.LANGS:
            data = file["languages"][lang]

            for form in config.FORMATS:
                temp = Path(config.BUILD_DIR / name / form / lang)
                temp.mkdir(parents=True, exist_ok=True)

                result = template.render(
                    f"template_{form}.tex", {**data, "image": config.PATH_TO_IMAGE}
                )

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
